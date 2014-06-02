#!/usr/bin/env python
#

import os.path
import os
import time
import filecmp
import sys
import shutil

def importfiles(arg, dirname, fnames):
    for fname in fnames:
        destpath = None
        srcfile = os.path.join(dirname, fname)
        created_time = time.gmtime(os.stat(srcfile).st_ctime)
        (banename, ext) = os.path.splitext(fname)
        if ext.lower() == ".jpg":
            destpath = os.path.join(arg,
                    "%04d" % (created_time.tm_year),
                    "%02d" % (created_time.tm_mon),
                    "%02d" % (created_time.tm_mday),
                    )
        elif ext.lower() == ".mov":
            destpath = os.path.join(arg,
                    "%04d" % (created_time.tm_year),
                    "%02d" % (created_time.tm_mon),
                    "%02d" % (created_time.tm_mday),
                    "movies"
                    )
        elif ext.lower() == ".cr2":
            destpath = os.path.join(arg,
                    "%04d" % (created_time.tm_year),
                    "%02d" % (created_time.tm_mon),
                    "%02d" % (created_time.tm_mday),
                    "CR2"
                    )
        if not destpath:
            return
        if not os.path.exists(destpath):
            os.makedirs(destpath)
        if not os.path.isdir(destpath):
            return
        srcfile = os.path.join(dirname, fname)
        destfile = os.path.join(destpath, fname.lower())
        if os.path.exists(destfile):
            cnt = 0;
            if filecmp.cmp(srcfile, destfile, shallow=False): # We have the file, don't copy
                print "have: %s as %s" % (srcfile, destfile)
                destfile = None
            else:
                print "diff: %s != %s" % (srcfile, destfile)
                while True:
                    newname = "%s-%d%s" % (banename, cnt, ext)
                    destfile = os.path.join(destpath, newname.lower() )
                    cnt += 1
                    if not os.path.exists(destfile):
                        break
                    if filecmp.cmp(srcfile, destfile, shallow=False):
                        print "have: %s as %s" % ( srcfile, destfile )
                        destfile = None
                        break


        if destfile:
            print "copy: %s -> %s" % (srcfile, destfile)
            shutil.copy2(srcfile, destfile)

if __name__ == "__main__":
    cachepath = "P:\\"
    cards = [ "g:\\DCIM", "/Volumes/NO NAME", "/Volumes/EOS_DIGITAL/" ] 

    for card in cards:
        os.path.walk( card, importfiles, cachepath)
