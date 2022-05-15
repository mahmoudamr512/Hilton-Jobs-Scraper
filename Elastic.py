from elasticsearch import helpers, Elasticsearch


class Elastic: 
    index_name = "hiltonjobs"
    links = []
    es = Elasticsearch([{'host':'localhost', 'port': 9200, 'scheme':"http", "use_ssl":False}], timeout=30, )

    """
        Elastic Search Wrapper class to deal with elasticsearch db.
    """
    def push_to_db(self):
        for link in self.links:
            if link is None:
                self.links.remove(link)
            else:
                elastic_query = json.dumps({
                    "query": {
                        "match_phrase": {
                            "title": link["title"]
                        }
                    }
                })
                res = self.es.search(index=self.index_name)
                if  res['hits']['total']['value'] != "0":
                    self.links.remove(link)
        helpers.bulk(self.es, self.links, index=self.index_name, raise_on_error=False)

    
    def __init__(self, links):
        self.links = links