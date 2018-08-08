import os
from .logging import getLogger
from .paths import Paths

logger = getLogger(__name__)
paths = Paths()


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
        self.facts = keyword_facts

        # Look for facts passed in via the environment.
        for key, value in os.environ.items():
            if key.startswith('TEDI_FACT_'):
                fact = key.split('_', 2)[-1]
                self[fact] = value

        # Provide some default facts.
        if 'image_tag' not in self:
            logger.debug('Default to image_tag: "latest"')
            self['image_tag'] = 'latest'

        logger.debug(f'New Factset: {self}')

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

    def get(self, key, default=None):
        return self.facts.get(key, default)

    def to_dict(self):
        """Return a dictionary representation of this Factset."""
        return self.copy().facts

    def update(self, *args, **kwargs):
        """Update with new facts, like Dict.update()."""
        self.facts.update(*args, **kwargs)

    def copy(self):
        """Return a copy of this Factset (not a reference to it)."""
        return Factset(**self.facts)
