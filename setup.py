import re
from setuptools import find_packages, setup

regex = re.compile(r"^__\w+__\s*=.*$")


def get_dunders():
    values = dict()
    with open("pipsync/__init__.py", "r") as f:
        dunders = list()
        for l in f.readlines():
            if regex.match(l):
                dunders.append(l)
        exec("\n".join(dunders), values)

    return values


def get_readme():
    with open("README.md", "r") as f:
        readme = f.read()

    return readme


about = get_dunders()

requirements = ["toml>=0.10.1", "pipenv>=2020.11.15"]

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=get_readme(),
    author=about["__author__"],
    author_email=about["__author_email__"],
    url="https://github.com/brysontyrrell/pipsync",
    license=about["__license__"],
    packages=find_packages(),
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=requirements,
    extras_require={},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    zip_safe=False,
    entry_points={"console_scripts": ["pipsync=pipsync:main"]},
)
