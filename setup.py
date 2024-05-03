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

NAME = "corbado-python-sdk"
VERSION: str = version
PYTHON_REQUIRES = ">=3.8"
REQUIRES = [
    "urllib3 >= 1.25.3, < 2.1.0",
    "python-dateutil",
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
    "pyopenssl",
    "PyJWT",
    "flask",
]

setup(
    name=NAME,
    version=VERSION,
    description="Corbado SDK",
    author="Corbado team",
    author_email="support@corbado.com",
    url="https://github.com/corbado/corbado-python",
    keywords=["Corbado", "Corbado Python SDK"],
    install_requires=REQUIRES,
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description=open(os.path.join(base_dir, "README.md"), encoding="utf-8").read(),
    package_data={"corbado_sdk": ["py.typed"]},
)
