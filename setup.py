from setuptools import find_packages, setup

setup(
    name="vsh",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        "ase",
        "numpy",
        "matplotlib",
        "pymatgen",
        "mp-api",
        "pyprocar",
        "pydantic",
    ],
    entry_points={"console_scripts": ["vsh = vsh.cli:main"]},
)
