from setuptools import setup


setup(name='tedi',
      version='0.6',
      description='Build tool for Elastic Stack Docker images',
      url='http://github.com/elastic/tedi',
      author='Elastic',
      author_email='infra@elastic.co',
      packages=['tedi'],
      python_requires='>=3.6<4',
      install_requires=[
          'click==6.7',
          'docker==3.4.1',
          'jinja2==2.10',
          'pyconfig>=3,<4',
          'pyyaml==3.13',
          'wget==3.2',
      ],
      tests_require=[
          'flake8==3.5.0',
          'mypy==0.560',
          'pytest-cov==2.5.1',
          'pytest-flake8==0.9.1',
          'pytest-mypy==0.3.0',
          'pytest==3.4.0',
      ],
      setup_requires=['pytest-runner==4.2.0'],
      entry_points='''
      [console_scripts]
      tedi=tedi.cli:cli
      ''')
