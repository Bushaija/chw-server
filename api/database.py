from sqlmodel import SQLModel, Session, create_engine

file_name = "chw2.db"
file_name_url = f"sqlite:///{file_name}"

engine = create_engine(file_name_url)

def create_tables_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

