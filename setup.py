from setuptools import setup


setup(name='pyqt-helper',
      version='0.0.1',
      description=(
          "PyQt UI Helper is a script for auto-generating boiler plate code for interacting with "
          "PyQt widgets, such as value getters and setters, widget connections, and slot functions."
      ),
      # https://pypi.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Software Development :: Code Generators',
          'Topic :: Software Development :: User Interfaces',
      ],
      keywords='python, python3, pyqt, pyqt5, ui',
      author='morefigs',
      author_email='morefigs@gmail.com',
      url='https://github.com/morefigs/pyqt-helper',
      license='MIT',
      packages=[],
      zip_safe=False,
      install_requires=[
          'pyqt5',
      ],
      extras_requires={
          'dev': []
      }
      )

# python3 -m pip install --user --upgrade setuptools wheel twine
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload dist/*
