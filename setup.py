from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='crowbar_package_manager',
    version='0.1.14',
    packages=find_packages(),
    install_requires=['toml', 'appdirs'],
    entry_points={
        'console_scripts': [
            'crowbar=crowbar:main',
            'cb=crowbar:main',
        ],
    },
    description = 'a local-first tool for managing python dependencies with pip',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
