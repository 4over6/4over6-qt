#!/usr/bin/env python

from setuptools import setup
from thu4over6.version import __version__

setup_cmdclass = {}

# Allow compilation of Qt .qrc, .ui and .ts files (build_qt command)
try:
    from setup_qt import build_qt
    setup_cmdclass['build_qt'] = build_qt
except ImportError:
    pass


setup(
    name="thu4over6",
    version=__version__,
    description="Client GUI for a custom 4over6 tunnel",
    long_description=open('README.rst').read(),
    author="Yichuan Gao",
    author_email="gaoyichuan000@gmail.com",
    url="https://github.com/4over6/4over6-qt",
    license="GNU GPLv3",
    packages=["thu4over6"],
    package_data={
        "thu4over6": [
            "4over6.png",
            "4over6_disabled.png",
            "*.ui",
        ],
    },
    data_files=[
        ("share/applications", ["4over6-qt.desktop"]),
        ("share/pixmaps", ["4over6.png"]),
    ],
    entry_points={
        "gui_scripts": [
            "thu4over6=thu4over6.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Networking",
    ],
    options={
        'build_qt': {
            'packages': ['thu4over6'],
        },
    },
    cmdclass=setup_cmdclass,
)
