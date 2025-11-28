# main.py
"""
Основна програма:
- читає data.csv
- читає config.ini
- для кожного параметра (temperature, humidity, pressure) виконує статистики згідно конфігурації
- виводить таблиці та зберігає results.json
Підтримує опціональні аргументи командного рядка --data та --config
"""

import csv
import json
import configparser
import argparse
import stats_utils as su

# Пороги різких перепадів
THRESHOLDS = {
    "temperature": 7,
    "humidity": 20,
    "pressure": 5000
}

def read_csv(filename):
    """Зчитує дані з CSV і повертає словник показників."""
    data = {"temperature": {}, "humidity": {}, "pressure": {}}

    try:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamp = row["timestamp"]
                data["temperature"][timestamp] = float(row["temperature"])
                data["humidity"][timestamp] = float(row["humidity"])
                data["pressure"][timestamp] = float(row["pressure"])
    except FileNotFoundError:
        print(f"Помилка: Файл '{filename}' не знайдено.")
        exit(1)

    return data


def read_config(filename):
    """Зчитує INI конфіг."""
    config = configparser.ConfigParser()
    config.read(filename, encoding='utf-8')

    settings = {}
    for section in config.sections():
        stats_list = [x.strip() for x in config[section]["stats"].split(",")]
        settings[section] = stats_list
    return settings


def build_cli_data(t, H, p):
    """Створює набір даних на основі CLI параметрів."""
    timestamp = "CLI_INPUT"

    return {
        "temperature": {timestamp: t},
        "humidity": {timestamp: H},
        "pressure": {timestamp: p}
    }


def main():
    # ПАРАМЕТРИ КОМАНДНОГО РЯДКА
    parser = argparse.ArgumentParser(description="Smart Home Stats with INI")
    parser.add_argument("-t", "--temperature", type=float)
    parser.add_argument("-H", "--humidity", type=float)
    parser.add_argument("-p", "--pressure", type=float)
    parser.add_argument("--data", default="data.csv", help="Файл даних CSV")
    parser.add_argument("--config", default="config.ini", help="Файл конфігурації INI")
    parser.add_argument("--md", action="store_true", help="Виводити таблиці у markdown форматі")

    args = parser.parse_args()

    # Чи працюємо у CLI режимі?
    cli_mode = (args.temperature is not None and
                args.humidity is not None and
                args.pressure is not None)

    # Режим 1 — CLI параметри
    if cli_mode:
        print("✔ Дані отримано з командного рядка")
        data = build_cli_data(args.temperature, args.humidity, args.pressure)

    else:
        # Режим 2 — зчитування CSV
        print(f"✔ Читання CSV: {args.data}")
        data = read_csv(args.data)

    # Зчитування INI
    config = read_config(args.config)
    results = {}

    # Обробка параметрів
    for param, values_dict in data.items():
        timestamps = list(values_dict.keys())
        values = list(values_dict.values())
        results[param] = {}

        # Друк таблиці з урахуванням формату
        su.print_table(param, values_dict, as_markdown=args.md)

        # Якщо параметр є у config.ini
        if param in config:
            for stat in config[param]:
                if stat == "average":
                    results[param]["average"] = su.get_average(values)
                elif stat == "min":
                    results[param]["min"] = su.get_min(values)
                elif stat == "max":
                    results[param]["max"] = su.get_max(values)
                elif stat == "median":
                    results[param]["median"] = su.get_median(values)
                elif stat == "jumps":
                    results[param]["jumps"] = su.detect_jumps(
                        values, timestamps, THRESHOLDS[param]
                    )

    # Збереження results.jso
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print("\n✔ Результати збережено у results.json")


if __name__ == "__main__":
    main()