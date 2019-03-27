from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='anafit',
      version='0.1.6',
      description='A toolbox providing interactive fitting tools for matplotlib',
      long_description=readme(),
      classifiers=[
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering'
      ],
      keywords='matplotlib fit',
      url='https://gitlab.com/xamcosta/Anafit',
      author='Maxime Costalonga',
      author_email='maxime.costalonga@gmail.com',
      packages=['anafit'],
      install_requires=[
          'matplotlib', 'numpy', 'scipy'#, 'PyQt5'
      ],
      include_package_data=True,
      zip_safe=False)
