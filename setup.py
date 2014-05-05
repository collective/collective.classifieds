from setuptools import setup, find_packages

version = '1.6'
long_description = (
    open('README.rst').read() + '\n' +
    # open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='collective.classifieds',
      version=version,
      description="Add classifieds to your Plone intranet or website.",
      long_description=long_description,
      classifiers=[
          'Framework :: Plone',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='classifieds sales intranet',
      author='Four Digits (ralph@fourdigits.nl)',
      author_email='ralph@fourdigits.nl',
      url='http://www.plone.org/products/classifieds',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
