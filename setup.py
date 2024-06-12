from setuptools import setup, find_packages

setup(
    name="kubesleuth",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description="Kubernetes Configuration Audit Tool",
    author="Benjamin Cody Pate",
    author_email="resume@epic-geek.net",
    url="https://github.com/thevanguardian/kubesleuth",
    packages=find_packages(),
    install_requires=[
        "kubernetes",
        "requests",
        "pyyaml",
        "jinja2"
    ],
    entry_points={
        'console_scripts': [
            'kubesleuth=kubesleuth:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
