import os
import sys
import time

if len(sys.argv) < 3:
    print("Usage: python simulate_attack.py <folder> <type>")
    sys.exit()

TARGET_FOLDER = sys.argv[1]
ATTACK_TYPE = sys.argv[2]

os.makedirs(TARGET_FOLDER, exist_ok=True)


def mass_creation():
    for i in range(200):
        with open(os.path.join(TARGET_FOLDER, f"file_{i}.txt"), "w") as f:
            f.write("data")
        time.sleep(0.005)


def mass_deletion():
    files = os.listdir(TARGET_FOLDER)
    for f in files:
        try:
            os.remove(os.path.join(TARGET_FOLDER, f))
            time.sleep(0.005)
        except:
            pass


def encryption_simulation():
    for i in range(200):
        with open(os.path.join(TARGET_FOLDER, f"enc_{i}.enc"), "w") as f:
            f.write("ENCRYPTED_DATA_" * 50)
        time.sleep(0.005)


if ATTACK_TYPE == "create":
    mass_creation()
elif ATTACK_TYPE == "delete":
    mass_deletion()
elif ATTACK_TYPE == "encrypt":
    encryption_simulation()
else:
    print("Unknown attack type")