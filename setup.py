from setuptools import setup

setup(
    name="notetaker",
    version="0.1.0",
    description="Simple CLI note-taking tool with interactive file browser",
    py_modules=["notetaker"],
    install_requires=[
        "simple-term-menu>=1.6.1",
    ],
    entry_points={
        "console_scripts": [
            "notetaker=notetaker:main",
        ],
    },
    python_requires=">=3.7",
)
