from codecs import open as codecs_open
from setuptools import setup, find_packages

setup(name='user-management-home-assistant',
      version='0.0.1',
      description=u"User Management for Home Assistant",
      long_description="User Management for Home Assistant",
      classifiers=[],
      keywords='',
      author=u"Gert-Jan van de Streek",
      author_email='g.j.streek@avisi.nl',
      url='https://github.com/keerts/pyninjasphere',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      test_suite='tests',
      install_requires=[
          'click',
          'pyyaml'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      user-management-home-assistant=LoginComponent.scripts.cli:cli
      """
      )
