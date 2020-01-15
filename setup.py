import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

with open("requirements.txt", 'r', encoding='utf-8') as f:
    dependencies = f.readlines()

setuptools.setup(
    name="fakemail",
    version="0.0.1",
    author="niceMachine",
    author_email="xuchaoo@gmail.com",
    description="temp mail|fake email",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jscrapy/fakemail",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependencies,

    python_requires='>=3.6',
)