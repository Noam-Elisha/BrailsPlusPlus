"""Setup file for the BRAILS++ package."""

import re
from setuptools import setup, find_packages

with open('brails/__init__.py', 'r', encoding='utf-8') as f:
    version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                        f.read(), re.M).group(1)
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='brails',
    version=version,
    description='BRAILS++: Building Regional Asset Inventories at Large Scale',
    long_description=long_description,
    author='NHERI SimCenter',
    author_email='nheri-simcenter@berkeley.edu',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'brails': ['py.typed', 'processors/vlm_image_classifier/clip/'
                   'bpe_simple_vocab_16e6.txt.gz']
    },
    install_requires=[
        'addict',
        'Cython',
        'ftfy',
        'matplotlib',
        'pillow',
        'plotly',
        'pycocotools',
        'requests',
        'seaborn',
        'shapely',
        'supervision',
        'timm',
        'torch',
        'torchvision',
        'transformers',
        'typing',
        'wget',
        'yapf',
        'webcolors',
        'opencv-python',
        'pandas'
    ],
    extras_require={
        'development': [
            'flake8',
            'pylint',
            'black',
            'pytest',
            'pytest-cov',
            'jupyter',
            'jupytext',
            'sphinx',
            'sphinx-autoapi',
            'nbsphinx',
            'flake8-rst',
            'flake8-rst-docstrings',
        ],
    },
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Environment :: Console',
        'Framework :: Jupyter',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering',
    ],
)

# devguide.python.org: Status of Python versions:
# Use to determine when to drop/add  support
# https://devguide.python.org/versions/
