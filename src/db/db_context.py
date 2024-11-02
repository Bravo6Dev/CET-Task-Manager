from sqlalchemy import engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import config
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_async_engine(config.DATABASE_URL, echo=True)
base = declarative_base()
async_session_local = sessionmaker(bind=engine, 
                                expire_on_commit=False,
                                class_=AsyncSession)

async def init_db():
    """
    Create all tables in database if not exist yet.

    This method should be called once on application startup.
    """
    async with engine.begin() as conn:
        conn.run_sync(base.metadata.create_all)

async def get_session():
    """
    Dependency to get a session for database operations.

    This dependency yields a db session that should be used as a context variable
    in path operation functions and other dependencies. It will make sure that the
    same session is used throughout a request and that it is properly closed after
    the request is finished.

    The session is also used to store data that is shared across the entire
    application, such as the user that is currently logged in.

    The session is created using the async_session_local session maker, which
    is a factory for creating new session objects. The session maker is
    configured to use the engine that is bound to the application.

    The session is created in the __aenter__ method of the session maker. The
    __aexit__ method is used to close the session.

    The session is not committed automatically. You need to explicitly call
    session.commit() to write changes to the database.

    The session is not closed automatically. You need to explicitly call
    session.close() to close the session.

    The session is not rolled back automatically. You need to explicitly call
    session.rollback() to roll back changes to the database.

    :yield: A session for database operations.
    :raises: Any exception that is raised while creating the session or
            while the session is being used.
    """
    try:
        async with async_session_local() as Session:
            yield Session
    except Exception as ex:
        raise ex