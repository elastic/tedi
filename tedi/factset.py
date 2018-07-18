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

        # If these environment variables are set, they will forcibly
        # override the corresponding facts.
        environment_facts = [
            'ARTIFACTS_DIR',
            'ELASTIC_VERSION',
            'STAGING_BUILD_NUM',
        ]
        for fact in environment_facts:
            if fact in os.environ:
                self[fact.lower()] = os.environ[fact]

        # Determine a Docker tag, like '6.3.0' or '6.4.0-SNAPSHOT'
        if 'staging_build_num' in self and 'elastic_version' in self:
            logger.debug('Setting image_tag to include staging_build_num.')
            self['image_tag'] = self['elastic_version'] + '-' + self['staging_build_num']
        elif 'elastic_version' in self:
            logger.debug('Setting image_tag to elastic_version.')
            self['image_tag'] = self['elastic_version']
        else:
            logger.warn('Setting image_tag to "latest"')
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
        return self.facts

    def update(self, *args, **kwargs):
        self.facts.update(*args, **kwargs)
