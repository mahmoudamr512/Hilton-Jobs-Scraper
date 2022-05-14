from elasticsearch import helpers, Elasticsearch




class Elastic: 
    es = Elasticsearch([{'host':'localhost', 'port': 9200, 'scheme':"http", "use_ssl":False}], timeout=30)

    """
        Elastic Search Wrapper class to deal with elasticsearch db.
    """
    def push_to_db(self):
        helpers.bulk(self.es, self.links, index=self.index_name)

    
    def __init__(self, links):
        self.links = links
