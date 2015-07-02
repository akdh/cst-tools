import luigi
import json
from boto.mturk.connection import MTurkConnection

class JsonTarget(luigi.LocalTarget):
    def json(self, mode='r', body=None):
        if mode == 'w':
            with self.open(mode) as f:
                json.dump(body, f)
        elif mode == 'r':
            with self.open(mode) as f:
                body = json.load(f)
            return body
        else:
            raise Exception('mode must be r/w')

class MTurkTask(luigi.Task):
    production = luigi.BoolParameter(default=False)

    def connection(self):
        return MTurkConnection(host=self.host())

    def host_slug(self):
        if self.production:
            return 'production'
        else:
            return 'sandbox'

    def host(self):
        if self.production:
            return 'mechanicalturk.amazonaws.com'
        else:
            return 'mechanicalturk.sandbox.amazonaws.com'
