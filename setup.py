# coding: utf-8

"""
    Corbado SDK

     # TODO: Package docstring


"""  # noqa: E501


from setuptools import find_namespace_packages, setup  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "corbado-python-sdk"
VERSION = "1.0.0"
PYTHON_REQUIRES = ">=3.8"
REQUIRES: list[str] = [
    "urllib3 >= 1.25.3, < 2.1.0",
    "python-dateutil",
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
    url="",
    keywords=["Corbado", "Corbado SDK"],
    install_requires=REQUIRES,
    # packages=find_packages(where="src", include=["corbado_python_sdk.generated"]),
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description="""\
     # TODO: description
    """,  # noqa: E501
    package_data={"corbado_sdk": ["py.typed"]},
)
