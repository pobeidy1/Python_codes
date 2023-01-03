# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 23:43:44 2022

@author: pobe4699
"""

from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'open nifti and crop it'
LONG_DESCRIPTION = ''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="crop_nifti_by_mouse_click", 
        version=VERSION,
        author="Peyman Obeidy",
        author_email="<peyman.obeidy@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['matplotlib','opencv-python','scipy','numpy', 'os','glob','tkinter ','nibabel '], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'nifti', 'multiple_file','crop','crop_image', 'MRI'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

#next
#1 python setup.py sdist bdist_wheel
#2 twine upload dist/*
