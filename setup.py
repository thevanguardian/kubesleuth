from setuptools import setup, find_packages

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
    install_requires=[
        "kubernetes>=25.3.0",
        "jinja2>=3.1.2",
        "markdown2>=2.4.2",
        "requests>=2.25.1"
    ],
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
