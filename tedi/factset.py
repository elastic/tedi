import os


class Factset(object):
    """A dictionary like object for storing facts

    A Factset is simply a mapping of strings to strings, as used for variable
    expansions in Jinja2 templates.

    The most useful feature of a Factset, when compared to a Dict, is that it
    sets various defaults at contruction time.

    Null (None) values are not supported in a Factset. Setting a fact to
    None deletes it entirely.
    """
    def __init__(self, **keyword_facts):
        self.facts = {}
        self['elastic_version'] = '6.2.2'

        # If these environment variables are set, they will become facts.
        # If they are not set, they will be None, and thus discarded.
        self['artifacts_dir'] = os.environ.get('ARTIFACTS_DIR')
        self['staging_build_num'] = os.environ.get('STAGING_BUILD_NUM')
        self.facts.update(dict(keyword_facts))

    def __repr__(self):
        return 'Factset(**%s)' % self.facts

    def __getitem__(self, key):
        return self.facts[key]

    def __setitem__(self, key, value):
        # Setting a fact to None deletes it.
        if value is None:
            try:
                del(self[key])
            except KeyError:
                pass
            finally:
                return

        # All facts should be string->string mappings, since they are intended
        # for use in Jinja2 templates.
        if not isinstance(key, str):
            raise ValueError
        if not isinstance(value, str):
            raise ValueError

        self.facts[key] = value

    def __delitem__(self, key):
        del(self.facts[key])

    def __iter__(self):
        for key in self.facts.keys():
            yield key

    def __contains__(self, key):
        return key in self.facts

    def to_dict(self):
        return self.facts

    def update(self, *args, **kwargs):
        self.facts.update(*args, **kwargs)
