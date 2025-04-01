from sqlalchemy import create_engine, Engine

from tock_genai_core.models.database.postgres.postgres_db_setting import PostgresSetting
from tock_genai_core.services.langchain.factory.factories import RelationalDBFactory
from tock_genai_core.services.security.security_service import fetch_secret_key_value


class PostgresFactory(RelationalDBFactory):
    """
    A factory class for creating a PostgreSQL database engine.

    Attributes
    ----------
    db_settings : PostgresSetting
        The settings used to configure the PostgreSQL database connection.
    """

    db_settings: PostgresSetting

    def get_database(self) -> Engine:
        """
        Creates a SQLAlchemy Engine instance for the PostgreSQL database.

        Returns:
            Engine: A SQLAlchemy Engine instance connected to the specified PostgreSQL database.
        """
        database_url = f"postgresql+psycopg2://{fetch_secret_key_value(self.db_settings.username)}:{fetch_secret_key_value(self.db_settings.password)}@{self.db_settings.db_url}/{self.db_settings.db_name}"
        engine = create_engine(database_url)

        return engine
