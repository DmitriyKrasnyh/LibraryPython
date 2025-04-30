import threading
import webbrowser
import time
import os
from app import app


def run_server():
    print("[*] Запуск Flask-сервера...")
    app.run(host="127.0.0.1", port=5000, use_reloader=False)  # use_reloader=False обязательно


def open_browser():
    time.sleep(2)
    webbrowser.open("http://localhost:5000")


def main():
    # Проверка, что не запускаем из PyInstaller-обработчика (иначе будет рекурсия)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        print("[*] Запущено как .exe")

    threading.Thread(target=run_server, daemon=True).start()
    open_browser()

    try:
        while True:
            time.sleep(1)  # Чтобы основной поток не завершался
    except KeyboardInterrupt:
        print("[*] Завершение работы.")


if __name__ == "__main__":
    import sys
    main()
