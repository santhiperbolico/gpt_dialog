from os import path

import setuptools

root_dir = path.abspath(path.dirname(path.dirname(__file__)))
with open(path.join(root_dir, "README.md"), "r") as fh:
    long_description = fh.read()
with open(path.join(root_dir, "src/requirements.txt")) as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="gpt_dialog",
    version="0.1.0",
    author="Santiago Arranz Sanz",
    author_email="santiago.arranz.sanz@gmail.com",
    description="Paquete con elementos para crear dialogos entre bots de GPT"
    "basados en la API de OpenAI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/santhiperbolico/gpt_dialog",
    install_requires=requirements,
    packages=setuptools.find_packages(".", exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    py_modules=["gpt_dialog"],
)
