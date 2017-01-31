#!/usr/bin/env python
import zipfile
import os
import shutil

def clean_dir(dir):
    if (dir!='/'):
        shutil.rmtree(dir)

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                while True:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if not drive:
                        break
                if word in (os.curdir, os.pardir, ''):
                    continue
                path = os.path.join(path, word)
            zf.extract(member, path)


def zip_files_to_gtfs(output_file,files):
    zipf = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        arch_name = os.path.basename(file)
        zipf.write(file,arch_name )