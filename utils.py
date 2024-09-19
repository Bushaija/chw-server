import pandas as pd 
from sqlmodel import Session, select

from server.models import HealthcareAdvisor, Stock
from server.database import engine, create_tables_db

df = pd.read_excel("./data/clean_data.xlsx")

def populate_tables():
    with Session(engine) as session:
        for index, row in df.iterrows():
            statement = select(HealthcareAdvisor).where(HealthcareAdvisor.full_name == row['fullname'])
            healthcare_advisor = session.exec(statement).first()
            if healthcare_advisor is None:
                healthcare_advisor = HealthcareAdvisor(
                    full_name=row['fullname'],
                    province=row['province'],
                    district=row['district'],
                    sector=row['sector'],
                    cell=row['cell']
                )
                session.add(healthcare_advisor)
                session.commit()
            
            stock = Stock(
                timestamp=row['timestamp'],
                stock_item_code=row['stock_item_code'],
                quantity=row['quantity'],
                status=row['status'],
                healthcare_advisor_id=healthcare_advisor.id
            )
            session.add(stock)
        session.commit()

if __name__ == "__main__":
    create_tables_db()
    populate_tables()