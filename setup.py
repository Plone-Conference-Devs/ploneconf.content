from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='ploneconf.content',
      version=version,
      description="IA for a conference website",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='conference, content, information, lorem ipsum',
      author='ploneconf',
      author_email='ploneconf@gmail.com',
      url='http://ploneconf.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ploneconf'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=[""],
      paster_plugins=[""],
      )
