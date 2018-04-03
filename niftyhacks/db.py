"""DB utilities to work with web.py databases.

This module provides utilities to inspect the database schema to find the
available tables, coulmns and constraints.

This is tested only on postgres db.
"""

class Schema:
    """Database Schema

    Provides access tables in the database.
    """
    def __init__(self, db):
        self.db = db

    def get_tables(self, table_schema='public', **filters):
        """Returns all tables in the database.

        :param table_schema: specified the table_schema to list tables in
        :return: list of table objects
        """
        rows = self.db.where("information_schema.tables", table_schema=table_schema, **filters)
        return [Table(self.db, row) for row in rows]

    def get_table(self, table_name, table_schema="public"):
        """Returns the table with specified table name.

        :param table_name: name of the table
        :param table_schema: name of the table schema
        :return: the table object
        """
        tables = self.get_tables(table_name=table_name, table_schema=table_schema)
        return tables and tables[0] or None

    def has_table(self, table_name, table_schema='public'):
        return self.get_table(table_name=table_name, table_schema=table_schema) is not None

class Table:
    """Table in a database.

    Important Attributes:
        - table_schema
        - table_name
        - table_type (VIEW, BASE TABLE)
    """
    def __init__(self, db, table_data):
        self.db = db
        self.__dict__.update(table_data)

    def get_columns(self, **filters):
        rows = self.db.where("information_schema.columns",
                table_schema=self.table_schema,
                table_name=self.table_name,
                **filters)
        return [Column(self, row) for row in rows]

    def get_column(self, column_name):
        columns = self.get_columns(column_name=column_name)
        return columns and columns[0] or None

    def has_column(self, column_name):
        return self.get_column(column_name) is not None

class Column:
    """A column in a database table.

    Important attributes:

        - column_name
        - data_type
        - column_default
        - is_nullable
    """
    def __init__(self, table, column_data):
        self.table = table
        self.__dict__.update(column_data)
