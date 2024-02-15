from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="msconsconverter",
    version="0.0.3",
    author="vdmitriyev",
    author_email="author@example.com",
    description="A converter from MSCONS (EDIFACT) to CSV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vdmitriyev/msconsconverter",
    packages=["msconsconverter"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

#packages=setuptools.find_packages(),