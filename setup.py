import setuptools

from kimaridraw.draw import VERSION

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kimaridraw",
    version=VERSION.version,
    author=VERSION.developer,
    author_email="kimariyb@163.com",
    description="A Python script that processes Multiwfn spectral data and plots various spectra.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=VERSION.website,
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'kimariplot=kimaridraw.draw:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
