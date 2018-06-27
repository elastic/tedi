## Development

### Initial setup

``` shell
git clone git@github.com:jarpy/tedi.git # FIXME
cd tedi
virtualenv --python=python3.6 venv
. venv/bin/activate
pip install -e .
```

### Running the tests

``` shell
python setup.py test
```

### Building the images

``` shell
tedi build
```

#### Debug logging

``` shell
TEDI_DEBUG=true tedi build
```
