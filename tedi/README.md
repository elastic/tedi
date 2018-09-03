# Developer README

## Design Goals

### Stage isolation
Each major step in the build process can be invoked in isolation. For example,
it should be possible to render all templates to create a Docker build context,
without invoking `docker build`.

### Stage transparency
The results of each stage shall be expressed as human-readable files on the
filesystem. These are accessible and familiar. It also allows "breaking in"
to the build process at various points when needed for debugging.

In particular, the _build context_ which is passed to Docker should be in
the standard on-disk format so that Tedi can be used to render the context
but is not required to execute the build (though it can do that, too).

### Minimal path manipulation
File and URL paths shall be as flat as possible. When a complex path must be
manipulated, it should done once only, with the intent of shortening,
flattening, simplifying the path.

### Get logic out of templates
If logic, particularly string manipulation, can be provided in Tedi that can
reduce the need for such logic in template files, Tedi should aim to provide it.

### Fail fast
Be strict about proceeding with each stage of the build. For example, some
systems silently continue after rendering null values to a template. That's
an error. Tedi should halt abruptly and loudly!

It's better to crash than to proceed in a indeterminate state. It's even better
to halt with a helpful message.

## Important Classes

Tedi is (mostly) object-oriented in implementation. Many of the most important
classes map closely to sections in the `tedi.yml` file. Where appropriate, those
classes will have a `from_config` class method which is a factory method for
instantiating, for example, an `Image` object from a block of YAML in the
`images` section of `tedi.yml`.

### Project
This is the highest level class. There will be only one `Project` object
per run. It maps to the _entire_ contents of `tedi.yml`.

### Image
The image class represents a single image build, and in particular the Docker
_build context_ that goes into it. In `tedi.yml`, each block declared under the
top-level `images` key becomes an `Image`.

An `Image` knows how to prepare a build context for itself, which consists
mostly of plain and template _files_ in a `Fileset`, and _assets_ (think tarballs)
that are managed by an `Assetset`.

### Fileset
A `Fileset` is all the hand-crafted files, directories, and templates that go
into a build. In practice, this is the contents of the `tedi` directory. The
`Fileset` does not include files that are downloaded or copied from elsewhere.


### Asset
An `Asset` defines a file that we need to get from somewhere else. It has a URL
and a local filename. `Assets` know how to _acquire_ themselves for use in the
build context, where they will show up as the specified local filename. HTTP
URLs will be downloaded and `file://` URLs will be copied into the build context
from elsewhere on the filesystem.

Assets are cached quite aggressively (perhaps excessively) to speed up
subsequent builds.

### Assetset
An `Assetset` is a collection of `Assets`. A Tedi build is invoked with a single
`Assetset`. The `Assets` defined therein will be acquired from their URLs and
then made available to the build context as local files.

`Assetset`s are created from blocks declared under the `asset_sets` key in
`tedi.yml`.

## Glossary

#### Build context
All the files that are provided to Docker when building an image. If you were to
run `docker build /tmp/soup`, then the build context would consist of:

* The whole directory structure of `/tmp/soup`, excluding `.j2` files.
* Rendered versions of all `.j2` files, with the extension removed.
* Copies (actually hard links) of any assets.

Each image declared in `tedi.yml` produces a complete build context, which is
stored in its own directory under `.tedi/build/`.

#### Fact
A datum that is needed to correctly build an image. Mostly used for
string expansions in Jinja2 templates, such as `Dockerfile` templates. The
current `elastic_version` is a good example of a fact. Facts are generally
defined in `tedi/tedi.yml` either on at the project level:

``` yaml
facts:
  color: green
```

or on a per-image basis:

``` yaml
images:
  gelato:
    facts:
      flavor: lemon
```

The can also be specifed on the command-line and through the environment. Check
the [user README](../README.md).

#### Tedi directory
The directory `tedi` within the project that is to be built. This directory
must contain `tedi.yml` and may contain template files and plain files.

#### Template file
A Jinja2 template file. Any file in the tedi directory with a `.j2` extension
will be processed through Jinja2, expanding any facts, before it is placed in
the build context (without the `.j2` extension).

#### Plain file
Any file in the tedi directory that does not have a `.j2` extension is simply
copied to the build context, preserving directory structure.
