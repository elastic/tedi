class Facts(object):
    def __init__(self):
        self.facts = {}
        self.facts['test_canary_fact'] = 'Cats can be right-pawed or left-pawed.'
        self.facts['elastic_version'] = '6.2.0'

    def get_all(self):
        return self.facts
