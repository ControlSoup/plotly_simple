from setuptools import find_packages, setup

# Auto generate install reqs

with open("requirements.txt", "r") as f:
    REQ_LINES = list(f.readlines())

for i in REQ_LINES:
    i += ","

setup(
    name="plotly_datadict",
    version="0.0.1",
    url="",
    author="Some Joe",
    author_email="joe.burge.iii@gmail.com",
    description="Thrust Modeling",
    install_requires=REQ_LINES,
)
