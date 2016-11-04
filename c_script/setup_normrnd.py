from distutils.core import setup, Extension

module = Extension('myNormrnd', sources = ['normrnd.c'])

setup (name = 'PackageName',
        version = '1.0',
        description = 'This is a package for normrnd',
        ext_modules = [module])
