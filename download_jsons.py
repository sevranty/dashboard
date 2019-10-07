import os
import wget
import ssl

print('=== START ===')

# CLEAR - PROJECT
print("# CLEAR-PROJECT")
filename = 'get-dashboard.json'

if os.path.exists(filename):
    os.remove(filename)
    print('REMOVE OK: '+filename)
else:
    print('File does not exists: '+filename)

# DOWNLOAD
print("# DOWNLOAD")
url = 'https://google.com'
print('WGET: Beginning file download with wget module')
ssl._create_default_https_context = ssl._create_unverified_context
wget.download(url, filename)

print('=== END ===')