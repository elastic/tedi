# Tedi: A Template Engine for Docker Images
Tedi is a tool for building Docker images for your project. It adds a templating
layer to your Dockerfile and any other files you choose. It then renders
those templates to a build context, and arranges for Docker to build it.

## Usage

Tedi is a CLI tool written in Python 3.6. It can be installed with Pip or run
as a Docker container.

If you are interested in using Tedi but not in developing it, Docker is the
recommend approach.

### Running in Docker

First, build an image of Tedi itself:

``` shell
docker build -t tedi .
```

Then you can run it with Docker:

``` shell
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock -v $MY_PROJECT:/mnt tedi build
```

* Because Tedi is itself a Docker client, we mount the Docker socket inside
  the container.
* We also mount the directory of whatever project we want to build on `/mnt`,
  where Tedi expects to find it. In particular, it expects to a find a `tedi.yml`
  there (see below).

#### Controlling verbosity

Verbose output, including the output from the Docker build, can be requested by
setting the `TEDI_DEBUG` environment variable to `true`:

``` shell
docker run -e TEDI_DEBUG=true [...] tedi build
```

#### Other commands
You can explore other commands via the built-in help:

``` shell
docker run --rm -it tedi --help
```

### Declaring `tedi.yml`

To build a Docker image for your project, create a file within your project at
`tedi/tedi.yml`.

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

  # Some facts have explicit support within Tedi. Setting the "docker_registry"
  # fact will give images fully qualifed names within that registry.
  # Like: "docker.elastic.co/elasticsearch/elasticsearch-oss"
  docker_registry: docker.elastic.co
```

### Build context files
Add any other files that are needed to complete your image to the `tedi`
directory. They will be provided as the Docker build context, via a staging
area in the hidden directory `.tedi`.

Both plain files and Jinja2 templates are supported.

The contents of `.tedi` are temporary and can be regenerated. You'll likely
want to add it to your `.gitignore` file.

#### Plain files
Any plain files, including arbitrarily deep directory structures will be copied
into the Docker build context.

#### Jinja2
Any files with a `.j2` extension will be rendered through the Jinja2 template
engine before being added to the Docker build context. Generally, you will want
to create (at least) a Dockerfile template at `tedi/Dockerfile.j2`.

The template engine will expand variables from the _facts_ defined in `tedi.yml`.

## Development

Tedi is written in Python 3.6 with tests in pytest. Some type annotations can be
found sprinkled around, for consumption by [mypy](http://mypy-lang.org/).

There's a [seperate README](./tedi/README.md) covering some of the design and
implementation details.

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
slow things like coverage reporting and mypy type checking.
``` shell
python setup.py testwatch
```
