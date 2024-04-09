from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='crowbar_package_manager',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'crowbar=crowbar:main',
            'cb=crowbar:main',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',  # This line is important for Markdown rendering on PyPI
)
