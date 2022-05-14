from elasticsearch import Elasticsearch, helpers

class Elastic: 
    es = Elasticsearch(([{'host':'localhost', 'port': 9200, 'scheme':"http"}]))

    """
        Elastic Search Wrapper class to deal with elasticsearch db.
    """
    def push_to_db(self):
        helpers.bulk(self.es, self.links, index='hiltonjobs', request_timeout=200)


    def __init__(self, links):
        self.links = links
