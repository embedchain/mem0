import logging

from embedchain.config.BaseConfig import BaseConfig
from embedchain.config.vectordbs import ElasticsearchDBConfig
from embedchain.models import VectorDatabases, VectorDimensions


class BaseAppConfig(BaseConfig):
    """
    Parent config to initialize an instance of `App`, `OpenSourceApp` or `CustomApp`.
    """

    def __init__(
        self,
        log_level=None,
        embedding_fn=None,
        db=None,
        host=None,
        port=None,
        id=None,
        collection_name=None,
        collect_metrics=True,
        db_type: VectorDatabases = None,
        vector_dim: VectorDimensions = None,
        es_config: ElasticsearchDBConfig = None,
    ):
        """
        :param log_level: Optional. (String) Debug level
        ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'].
        :param embedding_fn: Embedding function to use.
        :param db: Optional. (Vector) database instance to use for embeddings.
        :param host: Optional. Hostname for the database server.
        :param port: Optional. Port for the database server.
        :param id: Optional. ID of the app. Document metadata will have this id.
        :param collection_name: Optional. Collection name for the database.
        :param collect_metrics: Defaults to True. Send anonymous telemetry to improve embedchain.
        :param db_type: Optional. type of Vector database to use
        :param vector_dim: Vector dimension generated by embedding fn
        :param es_config: Optional. elasticsearch database config to be used for connection
        """
        self._setup_logging(log_level)
        self.collection_name = collection_name if collection_name else "embedchain_store"
        self.db = BaseAppConfig.get_db(
            db=db,
            embedding_fn=embedding_fn,
            host=host,
            port=port,
            db_type=db_type,
            vector_dim=vector_dim,
            collection_name=self.collection_name,
            es_config=es_config,
        )
        self.id = id
        self.collect_metrics = True if (collect_metrics is True or collect_metrics is None) else False
        return

    @staticmethod
    def get_db(db, embedding_fn, host, port, db_type, vector_dim, collection_name, es_config):
        """
        Get db based on db_type, db with default database (`ChromaDb`)
        :param Optional. (Vector) database to use for embeddings.
        :param embedding_fn: Embedding function to use in database.
        :param host: Optional. Hostname for the database server.
        :param port: Optional. Port for the database server.
        :param db_type: Optional. db type to use. Supported values (`es`, `chroma`)
        :param vector_dim: Vector dimension generated by embedding fn
        :param collection_name: Optional. Collection name for the database.
        :param es_config: Optional. elasticsearch database config to be used for connection
        :raises ValueError: BaseAppConfig knows no default embedding function.
        :returns: database instance
        """
        if db:
            return db

        if embedding_fn is None:
            raise ValueError("ChromaDb cannot be instantiated without an embedding function")

        if db_type == VectorDatabases.ELASTICSEARCH:
            from embedchain.vectordb.elasticsearch_db import ElasticsearchDB

            return ElasticsearchDB(
                embedding_fn=embedding_fn, vector_dim=vector_dim, collection_name=collection_name, es_config=es_config
            )

        from embedchain.vectordb.chroma_db import ChromaDB

        return ChromaDB(embedding_fn=embedding_fn, host=host, port=port)

    def _setup_logging(self, debug_level):
        level = logging.WARNING  # Default level
        if debug_level is not None:
            level = getattr(logging, debug_level.upper(), None)
            if not isinstance(level, int):
                raise ValueError(f"Invalid log level: {debug_level}")

        logging.basicConfig(format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s", level=level)
        self.logger = logging.getLogger(__name__)
        return
