from setuptools import setup


setup(name='tedi',
      version='0.1',
      description='Build tool for Elastic Stack Docker images',
      url='http://github.com/elastic/docker-images',
      author='Elastic',
      author_email='infra@elastic.co',
      packages=['tedi'],
      python_requires='>=3.4<=4',
      install_requires=[
          'click==6.7',
          'click-log==0.2.1',
          'docker==3.0.1',
          'jinja2==2.10',
          'pyconfig==3.2.3',
          'pyyaml==3.12',
      ],
      tests_require=[
          'pytest==3.4.1',
          'pytest-cov==2.5.1',
          'flake8==3.5.0',
          'pytest-flake8==0.9.1',
      ],
      setup_requires=['pytest-runner'],
      entry_points='''
      [console_scripts]
      tedi=tedi.cli:cli
      ''')
