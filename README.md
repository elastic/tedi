## Development

### Initial setup

``` shell
git clone git@github.com:elastic/tedi.git
cd tedi
virtualenv --python=python3.6 venv
. venv/bin/activate
pip install -e .
```

### Running the tests

``` shell
python setup.py test
```

#### Test Watcher

A small wrapper is provided to run a fast suite of tests continuously while
doing Test Driven Development. It uses pytest-watch with some options to skip
slow things like coverage reporting and MyPy type checking.
``` shell
python setup.py testwatch
```

### Building the images

``` shell
tedi build
```

#### Debug logging

``` shell
TEDI_DEBUG=true tedi build
```
