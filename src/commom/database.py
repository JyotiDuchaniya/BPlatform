import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class Database(object):
    session = None
    keyspace = "jyoti"
    cloud_config = {
            'secure_connect_bundle': '/Users/jyotiduchaniya/Desktop/BPlatform/secure-connect-users.zip'
    }
    auth_provider = PlainTextAuthProvider('eqQKOGgUlnsdyJnZTClqgycP', 'Wnl-iK27pJk6zNwOMoPW3TxpQ+k5UAiizPZaC2pckr_W6ZtSn,-Qpw-evvogYNnTrLEEW1Ak78-tpdO24I+YP35ZQ7.0HwR1eYO-z-kNzm+z.HFCtMHmAOSTD9gQXmCt')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)

    @staticmethod
    def initialize():
        Database.session = Database.cluster.connect()

    @staticmethod
    def insert(collection, data):
        return Database.session.execute(f"INSERT into jyoti.{collection} {data}")

    @staticmethod
    def find(collection, query=None):
        if query is None:
            row = Database.session.execute(f"select * from {Database.keyspace}.{collection}")
        else:
            row = Database.session.execute(f"select * from {Database.keyspace}.{collection} where {query} allow filtering").one()
        return row

    @staticmethod
    def find_length(collection):
        row = Database.session.execute(f"select count(*) from {Database.keyspace}.{collection}")
        return row

    @staticmethod
    def update(collection, data, query):
        row = Database.session.execute(f"update {Database.keyspace}.{collection} set {data} where {query}")
        print(row)

    @staticmethod
    def delete(collection, columns, query):
        Database.session.execute(f"delete {columns} from {Database.keyspace}.{collection} where {query}")
