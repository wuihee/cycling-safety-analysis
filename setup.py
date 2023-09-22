from setuptools import find_packages, setup

setup(
    name="cycling-safety-analysis",
    version="0.0.10",
    description="Interface to run sensors and publish to AWS IoT broker.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="Wuihee",
    author_email="wuihee@gmail.com",
    license="MIT",
)
