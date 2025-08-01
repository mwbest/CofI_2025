# setup.py
from setuptools import setup, find_packages

setup(
    name="cofi_reduction",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "ipywidgets",
        "pandas",
        "astropy", # 7.1.0 this version works
        "astro-pyvista", # 0.4.1 and this version works
        "ccdproc",
        "PyQt5",
        "PyQt6",
        "PySide6",
        "specutils",
        "ipydatagrid",
        # PyQt5, PyQt6,PySide6,
        # "photutils==2.20" This is a dependency in pyvista, so it's not required here.
        # Add any other dependencies needed by your package
    ],
)
