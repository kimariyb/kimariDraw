from setuptools import find_packages, setup

setup(
    name='kimariDraw',
    version='1.1.5',
    description='The application is used to draw the Energy Profile Map',
    author='kimariyb',
    author_email='kimariyb@163.com',
    url='https://github.com/kimariyb/kimariDraw',
    install_requires=[
        'numpy',
        'matplotlib',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kimariDraw = kimariDraw.main:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.9'
)
