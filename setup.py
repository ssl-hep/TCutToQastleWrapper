import setuptools
import codecs
import os.path

with open("README.md") as fh:
    long_description = fh.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")    

setuptools.setup(name = "tcut_to_qastle",    
    version = get_version("tcut_to_qastle/__init__.py"),
    packages = setuptools.find_packages(exclude=['tests']),
    description = "TCut selection for ROOT TTree to Qastle wrapper for ServiceX xAOD and Uproot transformer",
    long_description = long_description,
    long_description_content_type='text/markdown',
    author = "KyungEon Choi (UT Austin)",
    author_email = "kyungeonchoi@utexas.edu",
    url = "https://github.com/ssl-hep/TCutToQastleWrapper",
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