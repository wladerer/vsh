from setuptools import setup, find_packages

setup(
    name='vsh',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'ase',
        'numpy',
        'matplotlib',
        'pymatgen',
        'scipy'
    ]
)
