from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from .system_environment import SystemEnvironment

engine = create_engine(
            "clickhouse://default:@{host}:{port}/{scheme}".format(**SystemEnvironment().env['clickhouse']),
            encoding='utf8', convert_unicode=True, pool_size=10, max_overflow=0, pool_pre_ping=True)


session_options = {"autoflush": False, "autocommit": True, "expire_on_commit": False}
session = scoped_session(sessionmaker(bind=engine, **session_options))
