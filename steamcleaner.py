import fnmatch
import os
import shutil
import time
from winreg import *
import psutil


def registry_cleaner(root_reg, app_reg, sub_reg=""):
    print("===REGISTRY CLEANING===")
    if sub_reg == "":
        currentkey = app_reg
    else:
        currentkey = app_reg + "\\" + sub_reg
    ConnectRegistry(None, root_reg)
    try:
        open_key = OpenKey(root_reg, currentkey, 0, KEY_ALL_ACCESS | KEY_WOW64_64KEY)
    except FileNotFoundError as fnfe:
        print(f"[Not Found/Already Deleted] HKEY_CURRENT_USER\{currentkey}")
        return 0
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        return 1
    info_key = QueryInfoKey(open_key)
    for x in range(0, info_key[0]):
        subkey = EnumKey(open_key, 0)
        try:
            DeleteKey(open_key, subkey)
            print(f"Removed %s\\%s" % (currentkey, subkey))
        except:
            registry_cleaner(root_reg, currentkey, subkey)
    DeleteKey(open_key, "")
    open_key.Close()
    print("Removed %s" % (currentkey))
    return 0


def find_ssfn_files(path, pattern):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(name)
    return result


def folder_cleaner():
    print("===DIRECTORY CLEANING===")
    file_path = 'C:\Program Files (x86)\Steam'
    steam_local_path = fr'C:\Users\{os.getlogin()}\AppData\Local\Steam'
    files = ['appcache', 'userdata']
    files += find_ssfn_files(file_path, 'ssfn' + '*')
    # Delete - Program Filex (x86), appcache, userdata and ssfn files
    if os.path.exists(file_path):
        for f in files:
            if (f[0:4] == ('ssfn')):
                os.remove(file_path + "\\" + f)
            else:
                try:
                    shutil.rmtree(file_path + "\\" + f)
                except FileNotFoundError as fnfe:
                    print(f"[Not Found/Already Deleted] {fnfe.filename}")
                    # pass
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
    else:
        print("[Not Found/Already Deleted] " + file_path)
    # Delete - C:\Users\username\AppData\Local\Steam
    if os.path.exists(steam_local_path):
        try:
            shutil.rmtree(steam_local_path)
        except FileNotFoundError as fnfe:
            print(f"[Not Found/Already Deleted] {fnfe.filename}")
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    else:
        print("[Not Found/Already Deleted] " + steam_local_path)
    return 0


def steam_is_running():
    return "steam.exe" in (p.name() for p in psutil.process_iter())


def kill_process(process_name: str):
    try:
        PROCNAME = process_name
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == PROCNAME:
                proc.kill()
                time.sleep(3)
    except Exception as e:
        print(e)


def steam_cleaner():
    root_root = HKEY_CURRENT_USER
    root_path = 'SOFTWARE\Valve\Steam'
    registry_cleaner(root_root, root_path)
    folder_cleaner()
    print("===FINISHED===\nPlease verify manually that [Not Found/Already Deleted] paths have been cleared!")


def main():
    if steam_is_running():
        print("[ERROR] === STEAM IS RUNNING ===")
        close_steam_input = input("Close steam.exe? (yes = kill process | no = close steam manually): ")
        if close_steam_input == "yes":
            kill_process("steam.exe")
            steam_cleaner()
        else:
            print("Please EXIT from STEAM and run script again!")
            return 1
    else:
        steam_cleaner()


if __name__ == "__main__":
    main()
