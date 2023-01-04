from setuptools import setup, find_packages

import os

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-bulmaforms",
    version="0.1.0",
    description="Render django forms in bulma style",
    long_description="Please read the README.md file!",
    url="https://github.com/fechnert/django-bulmaforms",
    author="Tim Fechner",
    author_email="tim.fechner@mailbox.org",
    license="MIT License",
    packages=find_packages(),
    keywords="django-bulmaforms",
    include_package_data=True,
    zip_safe=False,
    install_requires=["Django>=1.11,<2.0"],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        # Replace these appropriately if you are stuck on Python 2.
        "Programming Language :: Python :: 3.x",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
