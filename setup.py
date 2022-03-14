#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from dj_generatortools/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("dj_generatortools", "__init__.py")


if sys.argv[-1] == "publish":
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == "tag":
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open("README.md").read()
requirements = open("requirements.txt").readlines()

setup(
    name="django-generatortools",
    version=version,
    description="""A set of tools to easily generate typical django models and code structure.""",
    long_description=readme,
    author="Thomas Weholt",
    author_email="thomas@weholt.org",
    url="https://github.com/weholt/django-generatortools",
    packages=[
        "dj_generatortools",
    ],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords="django, scaffolding, crud",
    entry_points={
        "console_scripts": [
            "add_model = dj_generatortools:main",
            "startbigapp = dj_generatortools:startbigapp",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
