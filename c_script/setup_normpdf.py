from distutils.core import setup, Extension

module = Extension('myPdf', sources = ['normpdf.c'])

setup (name = 'PackageName',
        version = '1.0',
        description = 'This is a package for normpdf',
        ext_modules = [module])
