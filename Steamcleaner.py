from winreg import *
import os
import shutil
import fnmatch

def registry_cleaner(root_reg, app_reg, sub_reg=""):

    if sub_reg=="":
        currentkey = app_reg
    else:
        currentkey = app_reg+"\\"+sub_reg

    
    ConnectRegistry(None,root_reg)
    open_key = OpenKey(root_reg, currentkey, 0, KEY_ALL_ACCESS | KEY_WOW64_64KEY)
    info_key = QueryInfoKey(open_key)

    for x in range (0, info_key[0]):
        subkey = EnumKey(open_key,0)
        try:
            DeleteKey(open_key,subkey)
            print("Removed %s\\%s"%(currentkey,subkey))
        except:
            registry_cleaner(root_reg,currentkey,subkey)
    
    DeleteKey(open_key,"")
    open_key.Close()
    print("Removed %s" % (currentkey))
    return 0

def find_ssfn_files(path, pattern):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name,pattern):
                result.append(name)
    return result

def folder_cleaner():
    file_path = 'C:\Program Files (x86)\Steam'
    files = ['appcache','userdata']

    files += find_ssfn_files(file_path,'ssfn'+'*')

    if os.path.exists(file_path):
        for f in files:
            if (f[0:4] == ('ssfn')):
                os.remove(file_path+"\\"+f)
            else:
                try:
                    shutil.rmtree(file_path+"\\"+f)
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
    else:
        print(file_path + " not found")
    return 0

def main():
    root_root = HKEY_CURRENT_USER
    root_path = 'SOFTWARE\Valve\Steam'

    registry_cleaner(root_root,root_path)
    folder_cleaner()
    return 0

if __name__ == "__main__":
    main()