import os
from contextlib import contextmanager
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from tock_genai_core.services.langchain.factory.db_factory import get_relational_db_factory
from tock_genai_core.models.orm.db_document import Base, DBDocument
from tock_genai_core.models.database.postgres.postgres_db_setting import PostgresSetting
from tock_genai_core.models.database.provider import RelationalDBProvider
from tock_genai_core.models.database.types import DBSetting
from tock_genai_core.models.security.raw_secret_key.raw_secret_key import RawSecretKey


@contextmanager
def get_session(engine: Engine):
    """
    Create a new session for the database and close it after usage.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def list_index(namespace: str) -> list[str]:
    """
    Retrieve a list of distinct indexes from the PostgreSQL database, filtered by 'namespace'.

    Parameters
    ----------
    namespace : str
        The namespace used to filter the index values.

    Returns
    -------
    List[str]
        A list of distinct index values found in the `DBDocument` table.
    """

    db_settings = get_postgres_settings()
    engine = get_relational_db_factory(db_settings=db_settings).get_database()
    # To map the class to the Database
    Base.metadata.create_all(bind=engine)

    with get_session(engine) as session:
        indexes = session.query(DBDocument.index).filter(DBDocument.namespace == namespace).distinct().all()
        return [index[0] for index in indexes]


def list_documents(index: str) -> list[str]:
    """
    Retrieve all document names with the specified index value.

    Parameters
    ----------
    index : str
        The index value to filter the documents by.

    Returns
    -------
    List[str]
        A list of names of documents matching the specified index.
    """
    db_settings = get_postgres_settings()
    engine = get_relational_db_factory(db_settings=db_settings).get_database()
    # To map the class to the Database
    Base.metadata.create_all(bind=engine)

    with get_session(engine) as session:
        document_names = session.query(DBDocument.name).filter(DBDocument.index == index).all()
        document_names_list = [name[0] for name in document_names]

    return document_names_list


def delete_document(index: str) -> None:
    """
    Delete all documents from the database with the specified index.

    Parameters
    ----------
    index : str
        The index value of the documents to delete.

    Returns
    -------
        None: This function does not return any value.
    """
    db_settings = get_postgres_settings()
    engine = get_relational_db_factory(db_settings=db_settings).get_database()
    # To map the class to the Database
    Base.metadata.create_all(bind=engine)

    with get_session(engine) as session:
        session.query(DBDocument).filter(DBDocument.index == index).delete(synchronize_session=False)
        session.commit()


def add_document_to_relational_db(db_settings: DBSetting, metadata: dict, filenames: list[str]) -> None:
    """
    Adds file(s) and file(s) informations (=metadata) to a relational database.

    Parameters
    ----------
        db_settings (DBSetting): Settings required to connect to the database.
        metadata (dict): Dictionary containing metadata to associate with the documents.
        filenames (list[str]): A list of uploaded files names containing.

    Returns
    -------
        None: This function does not return any value.
    """
    postgres_settings = get_postgres_settings()
    engine = get_relational_db_factory(db_settings=postgres_settings).get_database()

    Base.metadata.create_all(bind=engine)
    with get_session(engine) as session:
        for filename in filenames:
            document = DBDocument(
                index=db_settings.index, name=filename, doc_metadata=metadata, namespace=db_settings.namespace
            )
            session.add(document)

        session.commit()


def list_metadata(index: str, document: str) -> dict:
    """
    Retrieve the metadata for a specific document from the specified index in the database.

    Args:
        index (str): The name of the index from which to retrieve the document metadata.
        document (str): The name of the document for which to retrieve metadata.

    Returns
    -------
        Query: A SQLAlchemy Query object containing the metadata of the specified document.
                The results can be further processed to retrieve specific metadata fields.
    """
    postgres_settings = get_postgres_settings()
    engine = get_relational_db_factory(db_settings=postgres_settings).get_database()

    Base.metadata.create_all(bind=engine)
    with get_session(engine) as session:
        metadata = (
            session.query(DBDocument.doc_metadata)
            .filter(DBDocument.name == document, DBDocument.index == index)
            .first()
        )

    return metadata[0] if metadata else None


def get_postgres_settings() -> PostgresSetting:
    """
    Retrieves the PostgreSQL database engine configuration from environment variables.

    Environment Variables:
    - POSTGRES_DB: The name of the PostgreSQL database.
    - POSTGRES_HOST: The hostname or IP address where the PostgreSQL server is running.
    - POSTGRES_USER: The username to connect to the PostgreSQL database.
    - POSTGRES_PASSWORD: The password for the PostgreSQL user.

    Returns:
        PostgresSetting: A configuration object containing the database settings
        for connecting to the PostgreSQL database.
    """
    db_name = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST")
    user = RawSecretKey(type="Raw", value=os.getenv("POSTGRES_USER"))
    password = RawSecretKey(type="Raw", value=os.getenv("POSTGRES_PASSWORD"))

    db_settings = PostgresSetting(
        provider=RelationalDBProvider.PostgreSQL, db_name=db_name, db_url=host, username=user, password=password
    )

    return db_settings
