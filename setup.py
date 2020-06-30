import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(name = "tcut_to_qastle",
    version = "0.2",
    packages = setuptools.find_packages(exclude=['tests']),
    description = "TCut selection for ROOT TTree to Qastle wrapper for ServiceX xAOD and Uproot transformer",
    long_description = long_description,
    long_description_content_type='text/markdown',
    author = "KyungEon Choi (UT Austin)",
    author_email = "kyungeonchoi@utexas.edu",
    url = "https://github.com/kyungeonchoi/TCutToQastleWrapper",
    license = "BSD 3-clause",
    install_requires = ["qastle>=0.5"],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development",
        "Topic :: Utilities",
        ],
    platforms = "Any",
)