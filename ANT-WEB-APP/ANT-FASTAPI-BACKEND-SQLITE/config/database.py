import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

SQLACHEMY_DATABASE_URL = "sqlite:///./ant.db"

engine = _sql.create_engine(SQLACHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()