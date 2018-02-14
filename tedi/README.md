Design Goals
============

Stage isolation
---------------
Each major step in the build process can invoked in isolation.

Stage transparency
------------------
The results of each stage shall be expressed as human-readable files on the filesystem. These are accessible and familiar.

Minimal path manipulation
-------------------------
File and URL paths shall be as flat as possible. When complex paths must be manipulated, it should done once only, with the intent of shortening, flattening, simplifying the path.
