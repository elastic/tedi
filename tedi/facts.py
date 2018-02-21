import os


class Facts(object):
    def __init__(self):
        self.facts = {}
        self.set('test_canary_fact', 'Cats can be right-pawed or left-pawed.')
        self.set('elastic_version', '6.2.2')

        if 'ARTIFACTS_DIR' in os.environ:
            self.set('artifacts_dir', os.environ['ARTIFACTS_DIR'])
        else:
            self.set('artifacts_dir', None)

        if 'STAGING_BUILD_NUM' in os.environ:
            self.set('staging_build_num', os.environ['STAGING_BUILD_NUM'])
        else:
            self.set('staging_build_num', None)

    def set(self, key, value):
        self.facts[key] = value

    def get_all(self):
        return self.facts
