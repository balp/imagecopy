#!/usr/bin/env python
#
import argparse
import filecmp
import multiprocessing as mp
import os
import shutil
import time


def get_destination_path(cachepath, srcfile):
    """Return the desination folder for the file based on the image date."""
    destination_path = None
    created_time = time.gmtime(os.stat(srcfile).st_ctime)
    (basename, ext) = os.path.splitext(srcfile)
    if ext.lower() == ".jpg" or ext.lower() == ".cr2":
        destination_path = os.path.join(cachepath,
                "%04d" % (created_time.tm_year),
                "%02d" % (created_time.tm_mon),
                "%02d" % (created_time.tm_mday),
                )
    elif ext.lower() == ".mov":
        destination_path = os.path.join(cachepath,
                "%04d" % (created_time.tm_year),
                "%02d" % (created_time.tm_mon),
                "%02d" % (created_time.tm_mday),
                "movies"
                )
    return destination_path


def get_destination_filename(destpath, fname, srcfile):
    """Return the path the image should be copied to, or None if image exists"""

    destination_file = os.path.join(destpath, fname.lower())
    print("To: ", destination_file, destpath, fname)
    if os.path.exists(destination_file):
        cnt = 0
        if filecmp.cmp(srcfile, destination_file, shallow=False):
            print("have: %s as %s" % (srcfile, destination_file))
            destination_file = None
        else:
            print("diff: %s != %s" % (srcfile, destination_file))
            while True:
                (basename, ext) = os.path.splitext(fname)
                new_name = "%s-%d%s" % (basename, cnt, ext)
                destination_file = os.path.join(destpath, new_name.lower() )
                cnt += 1
                if not os.path.exists(destination_file):
                    break
                if filecmp.cmp(srcfile, destination_file, shallow=False):
                    print("have: %s as %s" % ( srcfile, destination_file ))
                    destination_file = None
                    break
    return destination_file


def stat_worker(input, output):
    for (base_dir, source_directory, file_name) in iter(input.get, 'STOP'):
        source_file_name = os.path.join(source_directory, file_name)
        destination_path = get_destination_path(base_dir, source_file_name)
        if not destination_path:
            continue
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        if not os.path.isdir(destination_path):
            continue
        destination_file_name = get_destination_filename(destination_path,
                                                        file_name,
                                                        source_file_name)
        if not destination_file_name:
            continue
        output.put((source_file_name, destination_file_name))
    output.put('STOP')

def copy_worker(input, output):
    for (source_name, destination_name) in iter(input.get, 'STOP'):
        print("copy: %s -> %s" % (source_name, destination_name))
        result = shutil.copy2(source_name, destination_name)
        output.put(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import images to archive")
    parser.add_argument('-b', '--basedir',
                        help='root of image archive', required=True)
    parser.add_argument('-c', '--card',
                        help='root of a card', action='append', required=True)
    args = parser.parse_args()
    base_dir = args.basedir
    cards = args.card
    n_workers = 5
    stat_queue = mp.Queue()
    copy_queue = mp.Queue()
    results_queue = mp.JoinableQueue()
    for card in cards:
        for directory_name, subdirlist, files in os.walk(card):
            for fname in files:
                stat_queue.put((base_dir, directory_name, fname))
    if n_workers > stat_queue.qsize():
        n_workers = stat_queue.qsize()
    for _ in range(n_workers):
        p = mp.Process(target=stat_worker,
                       args=(stat_queue, copy_queue,)).start()
    for _ in range(n_workers):
        p = mp.Process(target=copy_worker,
                       args=(copy_queue, results_queue)).start()
    for _ in range(n_workers):
        stat_queue.put('STOP')
    results_queue.join()
    stat_queue.close()
    copy_queue.close()
    results_queue.close()
