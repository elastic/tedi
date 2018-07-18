Design Goals
============

Stage isolation
---------------
Each major step in the build process can be invoked in isolation. For example,
it should be possible to render all templates to create a Docker build context,
without invoking `docker build`.

Stage transparency
------------------
The results of each stage shall be expressed as human-readable files on the
filesystem. These are accessible and familiar. It also allow "breaking in"
to the build process at various point when needed for debuggin.

In particular, the _build context_ which is passed to Docker should be in
the standard, on-disk format, so that Tedi can be used to render the context
but is not required to execute the build (though it can do that, too).

Minimal path manipulation
-------------------------
File and URL paths shall be as flat as possible. When complex paths must be
manipulated, it should done once only, with the intent of shortening,
flattening, simplifying the path.

Get logic out of templates
--------------------------
If logic, particularly string manipulation, can be provided in Tedi that can
reduce the need for such logic in template files, Tedi should aim to provide it.

Glossary
========

#### Build context
All the files that are provided to Docker when building an image. If you were
to run `docker build /tmp/soup`, then everything under `/tmp/soup` is the build
context.

Each image declared in `tedi.yml` produces a complete build context, which is
stored in it's own directory under the hidden `.tedi` directory.

#### Fact
A datum that is needed to correctly build an image. Mostly used for
string expansions in Jinja2 templates, such as the `Dockerfile` templates. The
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
