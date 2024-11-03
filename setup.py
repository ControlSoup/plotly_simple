from setuptools import setup

# Auto generate install reqs
with open("requirements.txt", "r") as f:
    REQ_LINES = [ i+"," for i in list(f.readlines())]

setup(
    name="plotly_simple",
    version="0.0.1",
    url="",
    author="Some Joe",
    author_email="joe.burge.iii@gmail.com",
    description="Thrust Modeling",
    install_requires=REQ_LINES,
)
