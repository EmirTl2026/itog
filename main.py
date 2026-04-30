import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

# --- Настройки ---
API_KEY = "ВАШ_API_КЛЮЧ"  # Замените на свой ключ с exchangerate-api.com
HISTORY_FILE = "history.json"


# --- Функции работы с API ---
def get_conversion_rate(from_currency, to_currency):
    """Получает курс конвертации из API."""
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("result") == "success":
            return data["conversion_rate"]
        else:
            messagebox.showerror("Ошибка API", data.get("error-type", "Неизвестная ошибка"))
            return None
    except Exception as e:
        messagebox.showerror("Ошибка сети", str(e))
        return None


# --- Функции работы с историей ---
def save_history(entry):
    """Сохраняет запись о конвертации в JSON-файл."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        else:
            history = []
        history.append(entry)
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю: {e}")


def load_history():
    """Загружает историю из JSON-файла."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        return []
    except Exception as e:
        messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить историю: {e}")
        return []


# --- Основная логика приложения ---
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер валют")

        # Валюты (можно расширить)
        self.currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]

        # Интерфейс
        self.create_widgets()
        self.load_history_to_table()

    def create_widgets(self):
        # Выбор валют
        ttk.Label(self.root, text="Из:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.from_currency_var = tk.StringVar(value="USD")
        ttk.Combobox(self.root, textvariable=self.from_currency_var,
                     values=self.currencies, state="readonly").grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="В:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.to_currency_var = tk.StringVar(value="EUR")
        ttk.Combobox(self.root, textvariable=self.to_currency_var,
                     values=self.currencies, state="readonly").grid(row=1, column=1, padx=5, pady=5)

        # Поле ввода суммы
        ttk.Label(self.root, text="Сумма:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка конвертации
        ttk.Button(self.root, text="Конвертировать", command=self.convert).grid(row=3, column=0, columnspan=2,
                                                                                pady=10)

        # Результат
        self.result_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Таблица истории
        self.history_tree = ttk.Treeview(self.root,
                                         columns=("from", "to", "amount", "result"),
                                         show="headings")

        self.history_tree.heading("from", text="Из")
        self.history_tree.heading("to", text="В")
        self.history_tree.heading("amount", text="Сумма")
        self.history_tree.heading("result", text="Результат")

        self.history_tree.grid(row=5, column=0, columnspan=2, pady=10)

    def is_valid_amount(self):
        amount_str = self.amount_entry.get()
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showwarning("Ошибка ввода", "Сумма должна быть положительным числом.")
                return False
            return True
        except ValueError:
            messagebox.showwarning("Ошибка ввода", "Введите корректное число.")
            return False

    def convert(self):
        if not self.is_valid_amount():
            return

        from_cur = self.from_currency_var.get()
        to_cur = self.to_currency_var.get()

        rate = get_conversion_rate(from_cur, to_cur)

        if rate is not None:
            amount = float(self.amount_entry.get())
            result = round(amount * rate, 2)

            # Отображение результата
            self.result_label.config(
                text=f"{amount} {from_cur} = {result} {to_cur} (Курс: 1 {from_cur} = {rate} {to_cur})"
            )

            # Сохранение в историю
            entry = {
                "from": from_cur,
                "to": to_cur,
                "amount": amount,
                "result": result,
                "rate": rate,
                "timestamp": "2026-04-30"  # Для реального приложения используйте datetime.now()
            }
            save_history(entry)

            # Добавление строки в таблицу (в начало)
            self.history_tree.insert("", 0,
                                     values=(from_cur, to_cur, amount, f"{result} {to_cur}"))

    def load_history_to_table(self):
        """Загружает историю из файла в таблицу при запуске."""
        history = load_history()

        # Очищаем таблицу перед загрузкой
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        for entry in history:
            self.history_tree.insert("", 0,
                                     values=(entry["from"],
                                             entry["to"],
                                             entry["amount"],
                                             f"{entry['result']} {entry['to']}"))


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()