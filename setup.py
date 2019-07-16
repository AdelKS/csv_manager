from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='csv_manager',
      version='0.2',
      description='A simple CSV importer/exporter with plotting capababilities with matplotlib',
      long_description=readme(),
      long_description_content_type="text/markdown",
      keywords='csv export import plot matplotlib',
      url='https://github.com/AdelKS/csv_manager',
      author='Adel KARA SLIMANE',
      author_email='adel.ks@zegrapher.com',
      license='The Unlicense',
      packages=['csv_manager'],
      install_requires=[
          'matplotlib', 'py_expression_eval'
      ],
      include_package_data=True,
      zip_safe=False)
