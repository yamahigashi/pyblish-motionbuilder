"""This setup script packages pyblish_motionbuilder"""

import os
import sys
from setuptools import setup, find_packages

version = []

with open("pyblish_motionbuilder/version.py") as f:
    for line in f:
        if not line.startswith("VERSION_"):
            continue
        _, v = line.rstrip().split(" = ")
        version += [v]

version = ".".join(version)


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.7",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
]


setup(
    name="pyblish-motionbuilder",
    version=version,
    packages=find_packages(),
    url="https://github.com/yamahigashi/pyblish-motionbuilder",
    license="LGPL",
    author="Takayoshi Matsumoto",
    author_email="yamahigashi@gmail.com",
    description="Maya Pyblish package",
    zip_safe=False,
    classifiers=classifiers,
    package_data={
        "pyblish_motionbuilder": [
            "plugins/*.py",
            "pythonpath/*.py"
        ]
    },
    install_requires=["pyblish-base>=1.4"],
)
