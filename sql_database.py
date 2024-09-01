from utils import log_exception, Validators, Executors
from sqlalchemy import (
    Engine,
    create_engine,
    MetaData,
)
from sqlalchemy.orm import declarative_base, Session


class SQLDatabase:
    def __init__(self, connection_url: str):
        self.engine: Engine = create_engine(connection_url)
        self.base = declarative_base(metadata=MetaData())
        self.validators = Validators(self.base.metadata)
        self.executors = Executors(Session(bind=self.engine))

    def create_tables(self):
        """Ensure all tables are created."""
        self.base.metadata.create_all(self.engine)

    def find_one(self, row, filters=None):
        table_name = "unknown"
        try:
            table_name, model = self.validators.table(row, filters)

            return self.executors.search_by(row, model, filters)
        except Exception as exc:
            log_exception("find_one", row, table_name)
            raise exc

    def save_one(self, row, filters=None):
        table_name = "unknown"
        try:
            table_name, model = self.validators.table(row, filters)
            query = self.executors.search_by(row, model, filters)
            self.validators.unique_row("save_one", row, query, table_name)

            self.executors.commit("saved one", row, table_name)
            return row
        except Exception as exc:
            log_exception("save_one", row, table_name)
            raise exc

    def update_one(self, row, updated_data_dict: dict, filters=None):
        table_name = "unknown"
        try:
            table_name, model = self.validators.table(row, filters)
            query = self.executors.search_by(row, model, filters)
            self.validators.unique_row("delete_one", row, query, table_name)

            self.executors.update_row(table_name, query, updated_data_dict)
            self.executors.commit("updated one", query, table_name)
            return query
        except Exception as exc:
            log_exception("update_one", row, table_name)
            raise exc

    def delete_one(self, row, filters=None):
        table_name = "unknown"
        try:
            table_name, model = self.validators.table(row, filters)
            query = self.executors.search_by(row, model, filters)
            self.validators.unique_row("delete_one", row, query, table_name)

            self.executors.commit("deleted one", query, table_name)

        except Exception as exc:
            log_exception("delete_one", row, table_name)
            raise exc

    def find_all(self, model, chunk_size=1000):
        try:
            return model.query.yield_per(chunk_size).all()
        except Exception as exc:
            log_exception("find_all", "all rows", model.__tablename__)
            raise exc

    def drop_table(self, model):
        try:
            self.executors.drop_table(model, self.engine)
        except Exception as exc:
            log_exception("drop_table", "all rows", model.__tablename__)
            raise exc
