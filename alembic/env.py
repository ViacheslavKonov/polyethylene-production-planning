from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from app.db import Base, get_engine_url
from app import models  # noqa: F401

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", get_engine_url().render_as_string(hide_password=False).replace('%', '%%'))
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=get_engine_url().render_as_string(hide_password=False), target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    from sqlalchemy import create_engine
    engine = create_engine(get_engine_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
