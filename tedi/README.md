Design Goals
============

Stage isolation
---------------
Each major step in the build process can be invoked in isolation.

Stage transparency
------------------
The results of each stage shall be expressed as human-readable files on the filesystem. These are accessible and familiar.

Minimal path manipulation
-------------------------
File and URL paths shall be as flat as possible. When complex paths must be manipulated, it should done once only, with the intent of shortening, flattening, simplifying the path.

Glossary
========

Fact: A datum that is needed to correctly build an image. Mostly used for string expansions in Jinja2 templates, such as the `Dockerfile` templates. The current `elastic_version` is a good example of a fact. Facts are generally defined in `tedi/tedi.yml` either on at the project level:

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
