#! /usr/bin/env python
import os
from distutils.core import setup
from distutils.extension import Extension

TINYCDB_DIR = 'src'
TINYCDB_FILE_NAMES = ['cdb_init.c', 'cdb_find.c', 'cdb_findnext.c', 'cdb_seq.c', 'cdb_seek.c', 'cdb_unpack.c',
                      'cdb_make_add.c', 'cdb_make_put.c', 'cdb_make.c', 'cdb_hash.c']
TINYCDB_FILES = [os.path.join(TINYCDB_DIR, name) for name in TINYCDB_FILE_NAMES]

setup(
    name="tinycdb",
    version="0.1",
    description="A Python wrapper for TinyCDB",
    author='Jeethu Rao',
    author_email='jeethu@jeethurao.com',

    ext_modules = [
        Extension(
            "tinycdb",
            ["generated/tinycdb.c"] + TINYCDB_FILES,
            include_dirs=[TINYCDB_DIR],
        )
    ]
)



