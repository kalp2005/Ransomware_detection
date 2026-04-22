import os
import signal
import psutil
from utils.logger import log

def take_action():
    log("⚠️ Threat detected! Taking action...")

    for proc in psutil.process_iter(['pid', 'cpu_percent']):
        try:
            if proc.info['cpu_percent'] > 70:
                os.kill(proc.info['pid'], signal.SIGTERM)
                log(f"Killed process: {proc.info['pid']}")
        except:
            pass