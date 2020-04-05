import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='python-can-pegasus',  
    version='0.1',
    #scripts=['dokr'] ,
    entry_points={
        'can.interface': [
            "pegasus=PegasusBus:PegasusBus",
        ]
    },
    author="Christian Gagneraud",
    author_email="christian.gagneraud@navico.com",
    description="Navico Pegasus CAN interface module for python-can",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="ssh://git@bitbucket.navico.com/~christian.gagneraud/pegasus-linux-poc.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['python-can', 'pyusb'],
    python_requires='>=3.6',
 )
