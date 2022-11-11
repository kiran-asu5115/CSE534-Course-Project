from elasticsearch import Elasticsearch


class GetMetrics:
    def __init__(self):
        # Instantiate a client instance
        client = Elasticsearch("http://localhost:9200")
        # Call an API, in this example `info()`
        print(client.info())


