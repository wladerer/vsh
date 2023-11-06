from setuptools import setup, find_packages

setup(
    name='vsh',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'ase',
        'numpy',
        'matplotlib',
        'pymatgen',
        'mp-api',
        'pyprocar'
    ],
    entry_points={
        'console_scripts': [
            'vsh = vsh:main'
        ]
    }
)
