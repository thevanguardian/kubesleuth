from setuptools import setup, find_packages
from kubesleuth.version import __version__

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="kubesleuth",
    version=__version__,
    description="A tool for auditing Kubernetes clusters for misconfigurations, security issues, and best practices.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Benjamin Cody Pate",
    author_email="resume@epic-geek.net",
    url="https://github.com/thevanguardian/kubesleuth",
    packages=find_packages(include=['kubesleuth', 'kubesleuth.*']),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'kubesleuth=kubesleuth.kubesleuth:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
