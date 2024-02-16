import os

from setuptools import find_packages, setup


def get_long_description() -> str:
    content = None
    with open("README.md", "r") as f:
        content = f.read()
    return content


def get_install_requires(fname: str = "requirements.txt"):
    """Returns requirements.txt parsed to a list"""
    targets = []
    if os.path.exists(fname):
        with open(fname, "r") as f:
            targets = f.read().splitlines()
    else:
        raise Exception(f"File with requirements was NOT found: {fname}")
    return targets


setup(
    name="msconsconverter",
    version="1.2.0",
    author="vdmitriyev",
    description="Converts MSCONS (EDIFACT) format in CSV",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/vdmitriyev/msconsconverter",
    packages=find_packages(exclude=["data"], include=["msconsconverter"]),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=get_install_requires("requirements.txt"),
	test_suite='tests'
)
