from distutils.core import setup
import sys
import clu

if '--doctest-modules' not in sys.argv:
    setup(name='clu',
          version=clu.__version__,
          description="Conversion betwen length units.",
          long_description=clu.__doc__,
          author=clu.__author__,
          author_email=clu.__contact__,
          license=clu.__license__,
          url='https://github.com/timp21337/PyCLU',
          classifiers=["Development Status :: 0.1 - Beta",
                       "Intended Audience :: Developers",
                       "Intended Audience :: Science/Research",
                       "Intended Audience :: System Administrators",
                       "License :: OSI Approved :: Python Software Foundation License",
                       "Natural Language :: English",
                       "Operating System :: OS Independent",
                       "Programming Language :: Python",
                       "Topic :: Scientific/Engineering",
                       "Topic :: Software Development :: Libraries :: Python Modules",
                       "Topic :: Utilities"],
          packages=['clu', 'clu.tests'],
          platforms=["all"],
          provides=['clu'],
          )