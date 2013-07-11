#!/usr/bin/env python
#
#

import os
import os.path
import shutil
import stat
import time

def copy_images(targetdir, dirname, names):
    for fname in names:
        dest = None
        srcname =  os.path.join(dirname, fname)
        created = os.stat( srcname ).st_ctime
        created_time = time.gmtime(created)
        (name, fext) = os.path.splitext(fname)
        if fext.lower() == ".jpg":
            dest = os.path.join(targetdir,
                    str(created_time.tm_year),
                    "%02d"%(created_time.tm_mon),
                    "%02d"%(created_time.tm_mday))
        elif fext.lower() == ".cr2":
            dest = os.path.join(targetdir,
                    str(created_time.tm_year),
                    "%02d"%(created_time.tm_mon),
                    "%02d"%(created_time.tm_mday),
                    "CR2")
        if dest:
            if not os.path.exists(dest):
                os.makedirs(dest)
            if os.path.isdir(dest):
                destname = os.path.join(dest, fname)
                if os.path.exists( destname ):
                    print "%s exist doesn't copy %s" % (destname, srcname)
                else:
                    print "copy %s -> %s" % (srcname, destname)
                    shutil.copy2(srcname, destname )


if __name__ == "__main__":
    carddir = "F:\\DCIM"
    targetdir = "P:\\"
    os.path.walk(carddir, copy_images, targetdir)
