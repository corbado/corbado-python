# coding: utf-8

"""
Corbado SDK

 # TODO: Package docstring


"""  # noqa: E501
import os

from setuptools import find_namespace_packages, setup  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

base_dir: str = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(base_dir, "VERSION")) as version_file:
    version: str = version_file.read().strip()

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
]


NAME = "corbado-python-sdk"
VERSION: str = version
PYTHON_REQUIRES = ">=3.8"

INSTALL_REQUIRES = [
    "urllib3 >= 1.25.3",
    "python-dateutil",  # used in generated code
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
    "pyopenssl",
    "PyJWT",
    "flask",
]
tox_requires = ["tox"]
tox_gh_requires = ["tox-gh>=1.2"]
flake8_requires = [
    "flake8",
    "pep8-naming",  # naming conventions check
    "flake8-builtins",
    "flake8-bugbear",
    "flake8-isort",  # check if import is sorted
    "darglint",
    "flake8-bandit",  # security check
    "flake8-return",
    "flake8-docstring-checker",  # enforce docstring
]

test_requires = ["pytest~=7.1.3", "pytest-cov>=2.8.1", "pytest-randomly>=3.12.0"]

setup(
    name=NAME,
    version=VERSION,
    description="Corbado SDK",
    author="Corbado team",
    author_email="support@corbado.com",
    url="https://github.com/corbado/corbado-python",
    keywords=["Corbado", "Corbado Python SDK"],
    install_requires=INSTALL_REQUIRES,
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    extra_requires={
        "gh": flake8_requires + tox_requires + test_requires + tox_gh_requires,
        "dev": flake8_requires + tox_requires + test_requires,
        "test": test_requires,
        "flake8": flake8_requires,
    },
    classifiers=CLASSIFIERS,
    long_description_content_type="text/markdown",
    long_description=open(os.path.join(base_dir, "README.md"), encoding="utf-8").read(),
    package_data={"corbado_sdk": ["py.typed"]},
)
