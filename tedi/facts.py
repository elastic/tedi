class Facts(object):
    def __init__(self):
        self.facts = {}
        self.set('test_canary_fact', 'Cats can be right-pawed or left-pawed.')
        self.set('elastic_version', '6.2.0')

    def set(self, key, value):
        self.facts[key] = value

    def get_all(self):
        return self.facts
