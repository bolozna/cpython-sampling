from distutils.core import setup, Extension
setup(name='_crandom', version='1.0',  \
      ext_modules=[Extension('_crandom', ['crandom.c'])])
