# coding=utf-8
"""
SETUP DISTRIBUTION

GLFW-TOOLBOX
Toolbox for GLFW Graphic Library.

MIT License
Copyright (c) 2019 Pablo Pizarro R.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Library imports
from setuptools import setup
from glfwToolbox.about import __author__, __description__, __email__, __url__, __version__

with open('README.md') as f:
    long_description = f.read()

setup(
    author=__author__,
    author_email=__email__,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: glfw'
    ],
    description=__description__,
    include_package_data=True,
    install_requires=['numpy', 'PyOpenGL', 'glfw', 'PIL', 'matplotlib'],
    license='MIT',
    long_description=long_description,
    name='glfw-toolbox',
    packages=['glfwToolbox'],
    url=__url__,
    version=__version__
)
