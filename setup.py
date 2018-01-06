from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='anafit',
      version='0.1',
      description='A toolbox providing interactive fitting tools for matplotlib',
      long_description=readme(),
      classifiers=[
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering'
      ],
      keywords='matplotlib fit',
#      url='http://github.com/storborg/funniest',
      author='Maxime Costalonga',
#      author_email='',
#      license='',
      packages=['anafit'],
      install_requires=[
          'matplotlib', 'numpy', 'scipy', 'PyQt5', 'os', 'sys', 'json', 
          'functools'
      ],
#      test_suite='nose.collector',
#      tests_require=['nose', 'nose-cover3'],
      include_package_data=True,
      zip_safe=False)
