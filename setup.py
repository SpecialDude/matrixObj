import setuptools

with open("README.md", "r") as rm:
    README = rm.read()

setuptools.setup(
    name="matrixObj",
    packages=["matrixObj"],
    version="1.0.2",
    license="MIT",
    description="A simple matrix module for basic matrix mathematical operations",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Warith Adetayo",
    author_email="warithadetayo.awa@gmail.com",
    url="https://github.com/SpecialDude/matrixObj",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3"
)
