from setuptools import setup, find_packages

version = '0.1+perfact.3'

setup(name='Products.SimpleUserFolder',
      version=version,
      description="PerFact Version of the Zope Product SimpleUserFolder",
      long_description="""The Product SimpleUserFolder allows methods from the
Data.fs to provide the user list, user addition, modification and deletion,
and authorization.
""",
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Framework :: Zope :: 2",
        "Framework :: Zope :: 4"
      ],
      keywords='',
      author='PerFact Innovation GmbH & Co. KG',
      author_email='info@perfact.de',
      url='https://github.com/perfact/SimpleUserFolder',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      package_data={
        'Products.SimpleUserFolder': ['www/*', ],
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      namespace_packages=['Products'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
