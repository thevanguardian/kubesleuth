"""
This setup.py file is used to package and distribute the kubesleuth tool, which is a tool for auditing Kubernetes clusters for misconfigurations, security issues, and best practices.

The setup() function is used to define the package metadata, including the name, version, description, author, URL, and other details. The find_packages() function is used to automatically discover the Python packages that should be included in the distribution.

The parse_requirements() function is used to read the requirements from the requirements.txt file and include them as dependencies for the package.

The entry_points dictionary is used to define a console script entry point for the kubesleuth tool, which allows it to be executed from the command line.

The classifiers list is used to provide additional metadata about the package, such as the development status, intended audience, license, supported Python versions, and relevant topics.
"""
from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines if line.strip() and not line.startswith('#')]

setup(
    name="kubesleuth",
    version="0.1.1",
    description="A tool for auditing Kubernetes clusters for misconfigurations, security issues, and best practices.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Benjamin Cody Pate",
    author_email="resume@epic-geek.net",
    url="https://github.com/thevanguardian/kubesleuth",
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'kubesleuth=audit:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    python_requires='>=3.8',
    license="GPLv3",
)
