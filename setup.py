from setuptools import setup, find_packages

setup(
    name="SphereStats",
    version="0.1",
    author="Ghulam Abbas Zafari",
    description="A geospatial analysis and visualization library for spherical computations",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "cartopy",
        "shapely",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
