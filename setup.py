from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """Reads the requirements.txt and returns a list of packages."""
    with open(file_path) as f:
        requirements = [line.strip() for line in f if line.strip()]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name="LogGenie",
    version="0.1.0",
    author="Vinay Babu Gorantla",
    author_email="vinayc.gorantla@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
