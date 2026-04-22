import os
import sys
import time

if len(sys.argv) < 3:
    print("Usage: python simulate_attack.py <folder> <type>")
    sys.exit()

TARGET_FOLDER = sys.argv[1]
ATTACK_TYPE = sys.argv[2]

os.makedirs(TARGET_FOLDER, exist_ok=True)


def get_next_index(prefix, extension):
    """
    Finds next index to avoid overwriting files
    """
    existing = [
        f for f in os.listdir(TARGET_FOLDER)
        if f.startswith(prefix) and f.endswith(extension)
    ]

    if not existing:
        return 0

    nums = []
    for f in existing:
        try:
            num = int(f.replace(prefix, "").replace(extension, ""))
            nums.append(num)
        except:
            pass

    return max(nums) + 1 if nums else 0


# 🟡 MASS CREATION (NO OVERWRITE)
def mass_creation():
    start = get_next_index("file_", ".txt")

    for i in range(start, start + 100):
        with open(os.path.join(TARGET_FOLDER, f"file_{i}.txt"), "w") as f:
            f.write("data")
        time.sleep(0.02)  # realistic delay


# 🔴 MASS DELETION
def mass_deletion():
    files = os.listdir(TARGET_FOLDER)

    for f in files:
        try:
            os.remove(os.path.join(TARGET_FOLDER, f))
            time.sleep(0.01)
        except:
            pass


# 🟣 ENCRYPTION SIMULATION (NO OVERWRITE)
def encryption_simulation():
    start = get_next_index("enc_", ".enc")

    for i in range(start, start + 20):
        with open(os.path.join(TARGET_FOLDER, f"enc_{i}.enc"), "w") as f:
            f.write("ENCRYPTED_DATA_" * 100)
        time.sleep(0.02)


# 🔥 MIXED ATTACK (REALISTIC)
def mixed_attack():
    mass_creation()
    time.sleep(1)
    encryption_simulation()
    time.sleep(1)
    mass_deletion()


# 🎯 RUN
if ATTACK_TYPE == "create":
    mass_creation()

elif ATTACK_TYPE == "delete":
    mass_deletion()

elif ATTACK_TYPE == "encrypt":
    encryption_simulation()

elif ATTACK_TYPE == "mixed":
    mixed_attack()

else:
    print("Unknown attack type")