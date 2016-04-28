# RUN ME WITH "python setup.py install"

from distutils.core import setup, Extension
setup(name='canv3d', version='1.0',  \
      ext_modules=[Extension('canv3d', ['canv3d.c'])])