#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    long_description = readme.read()

setup(
    name="django-staticfiles-downloader",
    version="1.1.0",
    description="Django staticfiles extension to download third-party static files",
    long_description=long_description,
    author="Jakub Dorňák",
    author_email="jakub.dornak@misli.cz",
    license="BSD",
    url="https://github.com/misli/django-staticfiles-downloader",
    packages=["staticfiles_downloader"],
    install_requires=["Django>=2", "pytz"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2",
        "Framework :: Django :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
