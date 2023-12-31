import setuptools

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kimaridraw",
    version="2.5.2.5",
    author="Kimariyb, Ryan Hsiun",
    author_email="kimariyb@163.com",
    description="A Python script that processes Multiwfn spectral data and plots various spectra.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kimariyb/kimariDraw",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'kimaridraw=KimariDraw.kimaridraw:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
