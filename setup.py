#! /usr/bin/env python
"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from glob import glob
from mimetypes import guess_type
import os
from pathlib import Path
from typing import Final

from get_version import get_version
from packaging.utils import canonicalize_name
from setuptools import find_packages, setup

here = Path(__file__).parent.resolve()
try:
    readme = next(iter(here.glob("README*")))
    long_description = readme.read_text()
    long_description_content_type = guess_type(readme)[0]
except StopIteration:
    long_description = ""
    long_description_content_type = None
REQUIREMENTS: Final = here / "requirements.txt"
try:
    install_requires = REQUIREMENTS.read_text().splitlines()
except FileNotFoundError:
    install_requires = []
extras_require = {}
for file in glob("requirements/*.txt"):
    name = os.path.basename(file)[:-4]
    extras_require[name] = Path(file).read_text().splitlines()
extras_require["all"] = sum(extras_require.values(), [])

VERSION: Final = get_version(__file__)
BINNAME: Final = "cgdemo"
NAME_: Final = "computer_graphics_demo"
NAME: Final = canonicalize_name(NAME_)
VCS_URL: Final = "https://github.com/Freed-Wu/computer-graphics-homework"

setup(
    name=NAME,
    version=VERSION,
    description="A demonstration of computer graphics",
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url=f"https://pypi.org/project/{NAME}",
    download_url=f"{VCS_URL}/tags",
    project_urls={
        "Bug Reports": f"{VCS_URL}/issues",
        "Source": VCS_URL,
    },
    author="wzy",
    author_email="wuzy01@qq.com",
    maintainer="wzy",
    maintainer_email="wuzy01@qq.com",
    license="GPLv3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
    ]
    + [
        f"Programming Language :: Python :: 3.{minor}"
        for minor in range(6, 10)
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            f"{BINNAME}={NAME_}.__main__:main",
        ],
    },
    keywords="python computer graphics",
)
