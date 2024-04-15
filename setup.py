from setuptools import setup

import versioneer

with open("requirements.txt") as install_requires_file:
    install_requires = install_requires_file.read().strip().split("\n")

with open("requirements-dev.txt") as dev_requires_file:
    dev_requires = dev_requires_file.read().strip().split("\n")

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="seatgeek-client",
    description="Python client for SeatGeek",
    author="Wade Glaser",
    author_email="Wade.Glaser@Gmail.com",
    url="https://github.com/WGlaser/seatgeek-client",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    install_requires=install_requires,
    packages=["seatgeek_client"],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
