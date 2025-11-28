# stats_utils.py
"""
Утиліти для обчислення статистик параметрів розумного будинку.
Містить: get_average, get_min, get_max, get_median, detect_jumps, print_table.
"""

from typing import List, Dict, Optional, Any
import statistics


def get_average(values: List[float]) -> Optional[float]:
    """Повертає середнє значення списку, округлене до 2 знаків або None якщо пустий список."""
    if not values:
        return None
    return round(statistics.mean(values), 2)


def get_min(values: List[float]) -> Optional[float]:
    """Повертає мінімальне значення або None якщо пусто."""
    return min(values) if values else None


def get_max(values: List[float]) -> Optional[float]:
    """Повертає максимальне значення або None якщо пусто."""
    return max(values) if values else None


def get_median(values: List[float]) -> Optional[float]:
    """Повертає медіану округлену до 2 знаків або None якщо пусто."""
    if not values:
        return None
    return round(statistics.median(values), 2)


def detect_jumps(values: List[float], timestamps: List[str], threshold: float) -> List[str]:
    """
    Виявляє різкі перепади між сусідніми значеннями.
    Якщо |current - previous| > threshold, то вважаємо, що в current timestamp стався "стрибок".
    Повертає список часових міток (timestamps[i]) де виникли такі стрибки.
    """
    jumps: List[str] = []
    if not values or not timestamps:
        return jumps
    # гарантуємо, що списки однакової довжини
    n = min(len(values), len(timestamps))
    for i in range(1, n):
        if abs(values[i] - values[i - 1]) > threshold:
            jumps.append(timestamps[i])
    return jumps


def print_table(parameter_name: str, data_dict: Dict[str, Any], as_markdown: bool = False) -> None:
    """
    Виводить таблицю параметра у псевдографіці або в markdown-форматі.
    - parameter_name: назва колонки (наприклад, "temperature")
    - data_dict: словник {timestamp: value}
    - as_markdown: якщо True — виводить markdown-таблицю
    """
    # Підготовка колонтитулів
    header_ts = "Timestamp"
    header_val = parameter_name

    if as_markdown:
        # Markdown-таблиця
        print(f"\n| {header_ts} | {header_val} |")
        print("|" + " ---------------- " + "|:---------:|")
        for ts, val in data_dict.items():
            print(f"| {ts} | {val:>8} |")
        return

    # Псевдографіка
    col1_w = max(len(header_ts), max((len(ts) for ts in data_dict), default=0)) + 2
    col2_w = max(len(header_val), 12) + 2
    sep = "+" + "-" * col1_w + "+" + "-" * col2_w + "+"

    print()
    print(sep)
    print(f"| {header_ts:<{col1_w-2}} | {header_val:<{col2_w-2}} |")
    print(sep)
    for ts, val in data_dict.items():
        # значення вирівнюємо ліво; формат числа однорідний
        print(f"| {ts:<{col1_w-2}} | {str(val):<{col2_w-2}} |")
    print(sep)
