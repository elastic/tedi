## Usage

### Running in Docker

The recommended way to run Tedi is within Docker:

``` shell
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/mnt tedi build
```

* Because Tedi is itself a Docker client, we mount the Docker socket inside.
* We also mount the directory of whatever project we want to build at `/mnt`,
  where Tedi expects to find it. In particular, it expects to a find a `tedi.yml`
  there (see below).

### `tedi.yml`

To build a Docker image for your project with, create a file at `./tedi/tedi.yml`.
Like this:

``` yaml
# Tedi can produce multiple images for a single project.
# Declare them under the "images" key.
images:
  # The image names should be the qualified path in your Docker registry.
  elasticsearch/elasticsearch-full:
    # Differences between images can be expressed with "facts". Facts are used
    # for variable expansion in template files, notably the Dockerfile template.
    facts:
      image_flavor: full

  elasticsearch/elasticsearch-oss:
    facts:
      image_flavor: oss

# Global facts apply to all images.
facts:
  elastic_version: 6.3.1
  docker_registry: docker.elastic.co
```

### Build context files
Add any other files that are needed to complete your image to `./tedi`. They
will be provided as the Docker build context, via a staging area in `./.tedi`.

Both plain files and Jinja2 templates are supported.

The contents of `.tedi` are temporary and can be regenerated. You'll likely want
to add it to your `.gitignore` file.

#### Plain files
Any plain files, including arbitrarily deep directory structures will be copied
into the Docker build context.

#### Jinja2
Any files with a `.j2` extension will be rendered through the Jinja2 template
engine before being added to the Docker build context. Generally, you will want
to create (at least) a Dockerfile template at `./tedi/Dockerfile.j2`.

The template engine will expand variables from the _facts_ defined in `tedi.yml`.

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
