# coding: utf-8


import os

from setuptools import find_namespace_packages, setup

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


NAME = "passkeys"
VERSION: str = version
PYTHON_REQUIRES = ">=3.8"

INSTALL_REQUIRES = [
    "urllib3 >= 1.25.3",
    "python-dateutil",  # used in generated code
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
    "pyopenssl",
    "PyJWT",
]

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
    classifiers=CLASSIFIERS,
    long_description_content_type="text/markdown",
    long_description=open(os.path.join(base_dir, "README.md"), encoding="utf-8").read(),
    package_data={"corbado_sdk": ["py.typed"]},
)
