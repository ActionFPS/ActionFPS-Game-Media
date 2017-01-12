# Running:
# $ python -m pip --user install -r requirements.txt
# $ python download.py
# $ find downloads|head
# downloads
# downloads/assaultcube-official
# downloads/assaultcube-official/audio
# downloads/assaultcube-official/audio/ambience
# downloads/assaultcube-official/audio/ambience/authors.txt
# downloads/assaultcube-official/audio/ambience/cavedrip.ogg
# downloads/assaultcube-official/audio/ambience/citynoisebirds.ogg
# 
import os
import urllib
import zipfile
RELEASE_YML_URL = "https://raw.githubusercontent.com/ActionFPS/ActionFPS-Game-Media/master/release.yml"
RELEASE_YML = "release.yml"
if not os.path.isfile(RELEASE_YML):
    urllib.urlretrieve(RELEASE_YML_URL, RELEASE_YML)

import yaml
with open(RELEASE_YML) as f:
    y = yaml.load(f.read())

def hashfile(fname, hash):
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

TARGET_DIR = "downloads"
import hashlib
import zipfile
import os
for id, desc in y.iteritems():

    TARGET_ZIP_FILE = "%s.tmp" % desc['shasum']
    if not os.path.isfile(TARGET_ZIP_FILE):
        urllib.urlretrieve(desc['zip'], TARGET_ZIP_FILE)
    hash = hashfile(TARGET_ZIP_FILE, hashlib.sha1())
    assert hash == desc['shasum']

    # Where we'll be storing this package
    package_target_dir = TARGET_DIR + "/" + id
    with zipfile.ZipFile(TARGET_ZIP_FILE, 'r') as myzip:
        for f in myzip.infolist():
            # Make sure we're looking only at a file
            if f.filename.startswith(desc['directory']) and not f.filename.endswith("/"):
                # Get the sub path eg 'packages/blah.xyz' instead of 'AC_1.2.3.4/packages/...'
                subname = f.filename[len(desc['directory']) + 1:]
                if subname not in desc['ignore']:
                    target_name = package_target_dir + "/" + subname
                    # Don't overwrite any more
                    if not os.path.isfile(target_name):
                        target_dir = "/".join(target_name.split("/")[:-1])
                        if not os.path.isdir(target_dir):
                            os.makedirs(target_dir)
                        print "%s -> %s -> %s" % (f.filename, subname, target_name)
                        with myzip.open(f, 'r') as sf:
                            import shutil
                            with open(target_name, 'w') as tf:
                                shutil.copyfileobj(sf, tf)
