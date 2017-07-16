#!/usr/bin/env python
#

import os.path
import os
import time
import filecmp
import sys
import shutil

def get_destination_path(cachepath, srcfile):
    destpath = None
    created_time = time.gmtime(os.stat(srcfile).st_ctime)
    (basename, ext) = os.path.splitext(fname)
    if ext.lower() == ".jpg":
        destpath = os.path.join(cachepath,
                "%04d" % (created_time.tm_year),
                "%02d" % (created_time.tm_mon),
                "%02d" % (created_time.tm_mday),
                )
    elif ext.lower() == ".mov":
        destpath = os.path.join(cachepath,
                "%04d" % (created_time.tm_year),
                "%02d" % (created_time.tm_mon),
                "%02d" % (created_time.tm_mday),
                "movies"
                )
    elif ext.lower() == ".cr2":
        destpath = os.path.join(cachepath,
                "%04d" % (created_time.tm_year),
                "%02d" % (created_time.tm_mon),
                "%02d" % (created_time.tm_mday),
                "CR2"
                )
    return destpath

def get_destination_filename(destpath, fname, srcfile):
    destfile = os.path.join(destpath, fname.lower())
    print("To: ", destfile, destpath, fname)
    if os.path.exists(destfile):
        cnt = 0;
        if filecmp.cmp(srcfile, destfile, shallow=False): # We have the file, don't copy
            print("have: %s as %s" % (srcfile, destfile))
            destfile = None
        else:
            print("diff: %s != %s" % (srcfile, destfile))
            while True:
                (basename, ext) = os.path.splitext(fname)
                newname = "%s-%d%s" % (basename, cnt, ext)
                destfile = os.path.join(destpath, newname.lower() )
                cnt += 1
                if not os.path.exists(destfile):
                    break
                if filecmp.cmp(srcfile, destfile, shallow=False):
                    print("have: %s as %s" % ( srcfile, destfile ))
                    destfile = None
                    break
    return destfile


def importfile(cachepath, dirname, fname):
    srcfile = os.path.join(dirname, fname)
    destpath = get_destination_path(cachepath, srcfile)
    if not destpath:
        return
    if not os.path.exists(destpath):
        os.makedirs(destpath)
    if not os.path.isdir(destpath):
        return
    destfile = get_destination_filename(destpath, fname, srcfile)

    if destfile:
        print("copy: %s -> %s" % (srcfile, destfile))
        shutil.copy2(srcfile, destfile)
    else:
        print("no copy: %s -> %s" % (srcfile, destfile))

if __name__ == "__main__":
    cachepath = "P:\\"
    cards = [ "g:\\DCIM", "/Volumes/NO NAME", "/Volumes/EOS_DIGITAL/" ] 

    for card in cards:
        for dirName, subdirlist, fileList in os.walk( card ):
            for fname in fileList:
                importfile(cachepath, dirName, fname)
