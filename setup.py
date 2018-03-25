from setuptools import setup, find_packages

setup(
    name="fun",
    version="0.0.dev0",
    packages=find_packages("src"),
    package_dir={"": "src"},
)
