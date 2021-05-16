from setuptools import setup

setup(
    name="zendesk-redactor",
    version="0.0.2",
    description="A command-line interface for Zendesk Ticket Redaction app",
    long_description=open("README.md").read(),
    author="Andrii Yurchuk",
    author_email="ay@mntw.re",
    license="Unlicense",
    url="https://github.com/Ch00k/zendesk-redactor",
    py_modules=["redactor"],
    install_requires=[
        "click==8.0.0",
        "requests==2.25.1",
    ],
    entry_points={"console_scripts": ["zredactor = redactor:redact"]},
    keywords="zendesk api ticket redaction",
)
