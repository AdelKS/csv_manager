from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='csv_manager',
      version='0.1',
      description='A simple CSV importer/exporter with plotting capababilities with matplotlib',
      long_description=readme(),
      keywords='csv export import plot matplotlib',
      url='https://github.com/AdelKS/csv_manager',
      author='Adel KARA SLIMANE',
      author_email='adel.ks@zegrapher.com',
      license='MIT',
      packages=['funniest'],
      install_requires=[
          'matplotlib', 'tkinter', 'py_expression_eval'
      ],
      include_package_data=True,
      zip_safe=False)
