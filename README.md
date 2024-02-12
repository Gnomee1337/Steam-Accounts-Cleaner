# Steam Accounts Cleaner

Script to clean steam account data from Windows:
1. Delete keys and subkeys from Windows Registry: `HKEY_CURRENT_USER\SOFTWARE\Valve\Steam\`
2. Delete 'ssfn' files, 'appcache' and 'userdata' directories from `C:\Program Files (x86)\Steam\`
3. Delete Steam directory and files from `C:\Users\%username%\AppData\Local\Steam\`

# Setup:
```
$ pip install -r requirements.txt
```

# Usage:
```
$ python Steamcleaner.py
