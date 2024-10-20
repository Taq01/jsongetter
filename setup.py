from setuptools import setup, find_packages

setup(
    name="jsongetter",
    version="0.1",
    packages=find_packages(),
    description="A library for dynamic search and retrieve data from JSON datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Taq01",
    author_email="taq.contact@proton.me",
    url="https://github.com/taq01/jsongetter",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
