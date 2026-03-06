from sqlalchemy import create_engine

DATABASE_URL = "oracle+cx_oracle://BOULDR_DEVELOPMENT:DevPwd99!@db:1521/?service_name=xe"

engine = create_engine(DATABASE_URL, echo=True)