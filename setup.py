from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='crowbar_package_manager',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'crowbar=crowbar:main',
            'cb=crowbar:main',
        ]
    }
)