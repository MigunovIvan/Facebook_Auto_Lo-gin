import sys
import os
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException
import pickle
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from tkinter import PhotoImage


# Функция для нахождения пути к ресурсам, когда программа работает как exe
def resource_path(relative_path):
    """ Получение абсолютного пути к ресурсу (например, к изображению) """
    try:
        # PyInstaller создаёт временную папку _MEIPASS для хранения ресурсов
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Путь к изображению для фона
BACKGROUND_IMAGE_PATH = resource_path("wall.png")

# Ваш основной код начинается здесь...

# Файл для сохранения логинов и паролей
ACCOUNTS_FILE = "last_logins.pkl"


# Функция для сохранения двух последних логинов и паролей
def save_last_accounts(accounts):
    with open(ACCOUNTS_FILE, "wb") as f:
        pickle.dump(accounts, f)


# Функция для загрузки двух последних логинов и паролей
def load_last_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "rb") as f:
            return pickle.load(f)
    return [{"email": None, "password": None}, {"email": None, "password": None}]


# Функция для входа через email и пароль
def login_facebook(browser, email, password):
    try:
        browser.get("https://www.facebook.com")
        email_input = browser.find_element(By.ID, "email")
        password_input = browser.find_element(By.ID, "pass")

        email_input.send_keys(email)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(3)
        return True
    except NoSuchElementException:
        messagebox.showerror("Ошибка", "Элементы не найдены. Проверьте ID для полей ввода.")
        return False


# Функция для ручного входа и сохранения логина и пароля
def manual_login():
    email = simpledialog.askstring("Вход в Facebook", "Введите ваш email:")
    password = simpledialog.askstring("Вход в Facebook", "Введите ваш пароль:", show="*")

    if email and password:
        browser = webdriver.Firefox(service=Service(log_path=os.devnull))  # Отключение логов Selenium
        if login_facebook(browser, email, password):
            # Обновляем список аккаунтов
            last_accounts = load_last_accounts()
            if last_accounts[0]["email"] is None:
                last_accounts[0] = {"email": email, "password": password}
            elif last_accounts[1]["email"] is None or last_accounts[1]["email"] != email:
                last_accounts[1] = {"email": email, "password": password}

            save_last_accounts(last_accounts)
            update_buttons()  # Обновляем тексты кнопок после сохранения данных
            messagebox.showinfo("Успех", "Вход выполнен и данные сохранены.")
        else:
            messagebox.showerror("Ошибка", "Не удалось выполнить вход в Facebook.")


# Функция, вызываемая при нажатии кнопки для аккаунта 1
def login_account1():
    last_accounts = load_last_accounts()
    if last_accounts[0]["email"]:
        browser = webdriver.Firefox(service=Service(log_path=os.devnull))
        if login_facebook(browser, last_accounts[0]["email"], last_accounts[0]["password"]):
            messagebox.showinfo("Успех", f"Вы вошли в аккаунт: {last_accounts[0]['email']}")
        else:
            messagebox.showerror("Ошибка", "Не удалось выполнить вход в аккаунт 1.")
    else:
        messagebox.showerror("Ошибка", "Аккаунт 1 не найден.")


# Функция, вызываемая при нажатии кнопки для аккаунта 2
def login_account2():
    last_accounts = load_last_accounts()
    if last_accounts[1]["email"]:
        browser = webdriver.Firefox(service=Service(log_path=os.devnull))
        if login_facebook(browser, last_accounts[1]["email"], last_accounts[1]["password"]):
            messagebox.showinfo("Успех", f"Вы вошли в аккаунт: {last_accounts[1]['email']}")
        else:
            messagebox.showerror("Ошибка", "Не удалось выполнить вход в аккаунт 2.")
    else:
        messagebox.showerror("Ошибка", "Аккаунт 2 не найден.")


# Функция для обновления текста на кнопках с именами аккаунтов
def update_buttons():
    last_accounts = load_last_accounts()
    if last_accounts[0]["email"]:
        button_account1.configure(text=f"Войти в аккаунт 1 ({last_accounts[0]['email']})")
    else:
        button_account1.configure(text="Войти в аккаунт 1 (не найден)")

    if last_accounts[1]["email"]:
        button_account2.configure(text=f"Войти в аккаунт 2 ({last_accounts[1]['email']})")
    else:
        button_account2.configure(text="Войти в аккаунт 2 (не найден)")


# Создание графического интерфейса с CustomTkinter
def create_gui():
    global button_account1, button_account2

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.title("Facebook Auto Login")
    app.geometry("500x400")

    # Установка фонового изображения (PNG)
    bg_image = PhotoImage(file=BACKGROUND_IMAGE_PATH)

    # Фрейм для изображения фона
    bg_label = ctk.CTkLabel(app, image=bg_image, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    label = ctk.CTkLabel(app, text="Выберите аккаунт для входа или войдите вручную:", font=("Arial", 16))
    label.pack(pady=20)

    # Кнопки для выбора аккаунтов с разными цветами
    button_account1 = ctk.CTkButton(app, text="Войти в аккаунт 1", command=login_account1, fg_color="blue",
                                    hover_color="lightblue")
    button_account1.pack(pady=10)

    button_account2 = ctk.CTkButton(app, text="Войти в аккаунт 2", command=login_account2, fg_color="green",
                                    hover_color="lightgreen")
    button_account2.pack(pady=10)

    # Кнопка для ручного входа
    button_manual_login = ctk.CTkButton(app, text="Войти вручную", command=manual_login, fg_color="purple",
                                        hover_color="lightpurple")
    button_manual_login.pack(pady=20)

    # Обновляем тексты кнопок с именами аккаунтов
    update_buttons()

    app.mainloop()


if __name__ == "__main__":
    create_gui()
