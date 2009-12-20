from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name="tinycdb",
    version="0.1",
    description="A Python wrapper for TinyCDB",
    author='Jeethu Rao',
    author_email='jeethu@jeethurao.com',
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("tinycdb", ["tinycdb.pyx"],
                             libraries=['cdb'])]
)



