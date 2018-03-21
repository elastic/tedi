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

Fact: A datum that is needed to correctly build an image. Mostly used for string expansions in Jinja2 templates, such as the `Dockerfile` templates. The current `elastic_version` is a good example of a fact. Global facts are defined in `facts.py`. Additional facts are defined on a per-_variant_ basis in `tedi.yml` files.

Variant: Each image has one or more variants. Each variant builds a separate image. In the case of multiple variants, they will tend to differ by the _facts_ that are passed the rendering stage. The variant is appended to the image name. Declaring a single variant with the special name 'default' suppresses this behavior.
