from setuptools import setup


setup(name='pyqt-helper',
      version='0.0.3',
      description="PyQt Helper auto-generates boiler plate code for interacting with PyQt widgets.",
      long_description=(
          "PyQt Helper is a script for auto-generating boiler plate code for interacting with PyQt "
          "widgets, such as value getters and setters, widget connections, and slot functions."
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
      keywords='python, python3, pyqt, pyqt5, ui, code-generation',
      author='morefigs',
      author_email='morefigs@gmail.com',
      url='https://github.com/morefigs/pyqt-helper',
      license='MIT',
      packages=[
          'pyqt_helper',
      ],
      zip_safe=False,
      install_requires=[
          'pyqt5',
      ],
      extras_requires={
          'dev': [
              'pytest',
          ]
      }
      )

# python -m pip install --user --upgrade setuptools wheel twine
# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
