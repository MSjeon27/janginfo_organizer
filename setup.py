#! /usr/bin/env python

from setuptools import setup, find_packages, Command

from distutils.command.build_py import build_py

setup(
    name             = 'janginfo_organizer',
    version          = '1.0.0',
    description      = 'Package for distribution',
    author           = 'msjeon27',
    author_email     = 'msjeon27@cau.ac.kr',
    url              = '',
    download_url     = '',
    install_requires = ['argparse', 'Bio'],
	include_package_data=True,
	packages=find_packages(),
    keywords         = ['JANGINFOORGANIZER', 'janginfoorganizer'],
    cmdclass         = {'build_py': build_py},
	scripts          = ['scripts/janginfo_organizer'],
    python_requires  = '>=3.6',
    zip_safe=False,
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
) 
