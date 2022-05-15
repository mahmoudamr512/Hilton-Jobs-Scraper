from elasticsearch import helpers, Elasticsearch
import json

class Elastic: 
    index_name = "hiltonjobs"
    links = []
    es = Elasticsearch([{'host':'localhost', 'port': 9200, 'scheme':"http", "use_ssl":False}], timeout=30 )

    """
        Elastic Search Wrapper class to deal with elasticsearch db.
    """
    def push_to_db(self):
        cleaned_list = []
        for link in self.links:
            if link is None:
               pass
            else:
                elastic_query = json.dumps({
                    "query": {
                        "match_phrase": {
                            "title": link["title"]
                        }
                    }
                })
                res = self.es.search(index=self.index_name)
                if  res['hits']['total']['value'] != 0:
                   pass
                else:
                    cleaned_list.append(link)
        helpers.bulk(self.es, cleaned_list, index=self.index_name, raise_on_error=False)

    def __init__(self, links):
        self.links = links
