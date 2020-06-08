from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="msconsconverter",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vdmitriyev/msconsconverter",
    packages=["msconsconverter"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Unknown",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

#packages=setuptools.find_packages(),