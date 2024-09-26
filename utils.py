import pickle
from datetime import datetime, timedelta
import pandas as pd 
from sqlmodel import Session, select

from server.models import HealthcareAdvisor, Stock
from server.database import engine, create_tables_db


df = pd.read_excel("./data/data.xlsx")

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def populate_tables():
    with Session(engine) as session:
        for index, row in df.iterrows():
            statement = select(HealthcareAdvisor).where(HealthcareAdvisor.full_name == row['fullname'])
            healthcare_advisor = session.exec(statement).first()
            if healthcare_advisor is None:
                healthcare_advisor = HealthcareAdvisor(
                    full_name=row['fullname'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    province=row['province'],
                    district=row['district'],
                    sector=row['sector'],
                    cell=row['cell']
                )
                session.add(healthcare_advisor)
                session.commit()
            
            stock = Stock(
                timestamp=row['timestamp'],
                year=row['year'],
                month=row['month'],
                stock_item_code=row['stock_item_code'],
                quantity=row['quantity'],
                status=row['status'],
                item_category=row['item_category'],
                healthcare_advisor_id=healthcare_advisor.id
            )
            session.add(stock) 
        session.commit()


def feature_encode(test_df):
    # Load the Excel data
    df = pd.read_excel("./data/data444.xlsx")
    df['FirstName'] = df['FirstName'].str.title()
    df['LastName'] = df['LastName'].str.title()
    # Get the current year and the next month
    today = datetime.today()
    next_month = (today.replace(day=1) + timedelta(days=32)).month  # Moves to the next month
    year_id = today.year if next_month != 1 else today.year + 1

    # Prepare data subsets
    df_prov = df[['Province', 'Province ID']].drop_duplicates()
    df_distr = df[['District', 'District ID']].drop_duplicates()
    df_sector = df[['Sector', 'Sector ID']].drop_duplicates()
    df_cell = df[['Cell', 'Cell ID']].drop_duplicates()
    df_name = df[['FirstName', 'LastName', 'FullName ID']].drop_duplicates()
    df_stock_type = df[['StockItemCode', 'StockItemCode ID']].drop_duplicates()

    # Find the corresponding IDs
    province_id = df_prov[df_prov['Province'] == test_df.iloc[:1,:].values[0,2].title()]['Province ID'].values
    district_id = df_distr[df_distr['District'] == test_df.iloc[:1,:].values[0,3].title()]['District ID'].values
    sector_id = df_sector[df_sector['Sector'] == test_df.iloc[:1,:].values[0,4].title()]['Sector ID'].values
    cell_id = df_cell[df_cell['Cell'] == test_df.iloc[:1,:].values[0,5].title()]['Cell ID'].values
    full_name_id = df_name[(df_name['FirstName'] == test_df.iloc[:1,:].values[0,0].title()) & (df_name['LastName'] == test_df.iloc[:1,:].values[0,1].title())]['FullName ID'].values
    stock_item_code_id = df_stock_type[df_stock_type['StockItemCode'] == test_df.iloc[:1,:].values[0,6]]['StockItemCode ID'].values
    print("encoded output: ", cell_id)

    # Return the IDs as a dictionary
    dict_id = {
        'Province ID': province_id[0] if province_id.size > 0 else None,
        'District ID': district_id[0] if district_id.size > 0 else None,
        'Sector ID': sector_id[0] if sector_id.size > 0 else None,
        'Cell ID': cell_id[0] if cell_id.size > 0 else None,
        'FullName ID': full_name_id[0] ,
        'StockItemCode ID': stock_item_code_id[0] if stock_item_code_id.size > 0 else None,
        'Year': year_id,
        'Month': next_month
    }
    id_list = list(dict_id.values())
    return dict_id

def predict(model, row):
    row_encoded = feature_encode(row)
    row_encoded_df = pd.DataFrame([row_encoded])
    row_prediction = model(row_encoded_df)
    return round(row_prediction[0])

if __name__ == "__main__":
    create_tables_db()
    populate_tables()
