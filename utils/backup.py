import os
import shutil

BACKUP_DIR = "backup"


def create_backup(source_folder):
    if os.path.exists(BACKUP_DIR):
        shutil.rmtree(BACKUP_DIR)

    shutil.copytree(source_folder, BACKUP_DIR)


def restore_backup(target_folder):
    if not os.path.exists(BACKUP_DIR):
        return

    # Remove current folder contents
    for filename in os.listdir(target_folder):
        file_path = os.path.join(target_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                shutil.rmtree(file_path)
        except:
            pass

    # Restore backup
    for item in os.listdir(BACKUP_DIR):
        src = os.path.join(BACKUP_DIR, item)
        dst = os.path.join(target_folder, item)

        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)