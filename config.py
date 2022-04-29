import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                             "postgresql://postgres:root@localhost/ecom")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PAGE_SIZE = 25
    PROMOTED_PER_PAGE = 2
    PROMOTED_SLOTS = [2, 16]
    AUTHOR_LENGTH = 8
    # db
    POSTGRES_USER = "test"
    POSTGRES_PASSWORD = "test"
    POSTGRES_DB = "test"
    SQL_HOST = "db"
    SQL_PORT = 5432

    # @property
    # def database_uri(self):
    #     return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}" \
    #            f"@{self.SQL_HOST}:{self.SQL_PORT}/{self.POSTGRES_DB}"
