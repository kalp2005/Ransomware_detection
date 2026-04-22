import datetime
import os

os.makedirs("logs", exist_ok=True)

def log(message):
    with open("logs/system.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")