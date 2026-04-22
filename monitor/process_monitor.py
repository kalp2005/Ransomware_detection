import psutil
from utils.logger import log

def check_process():
    suspicious_count = 0

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            if proc.info['cpu_percent'] > 70:
                suspicious_count += 1
                log(f"High CPU: {proc.info}")
        except:
            pass

    return suspicious_count