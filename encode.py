import pandas as pd
from datetime import datetime, timedelta

def collect_ids(test_df):
    # Load the Excel data
    df = pd.read_excel("data444.xlsx")
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

# import pandas as pd
# import pickle
# from datetime import datetime, timedelta

# def collect_ids(first_name, last_name, province, district, sector, cell, commodity_type):
#     # Load the Excel data
#     df = pd.read_excel("data444.xlsx")

#     # Get the current year and the next month
#     today = datetime.today()
#     next_month = (today.replace(day=1) + timedelta(days=32)).month  # Moves to the next month
#     year_id = today.year if next_month != 1 else today.year + 1

#     # Prepare data subsets
#     df_prov = df[['Province', 'Province ID']].drop_duplicates()
#     df_distr = df[['District', 'District ID']].drop_duplicates()
#     df_sector = df[['Sector', 'Sector ID']].drop_duplicates()
#     df_cell = df[['Cell', 'Cell ID']].drop_duplicates()
#     df_name = df[['FirstName', 'LastName', 'FullName ID']].drop_duplicates()
#     df_stock_type = df[['StockItemCode', 'StockItemCode ID']].drop_duplicates()

#     # Find the corresponding IDs
#     province_id = df_prov[df_prov['Province'] == province]['Province ID'].values
#     district_id = df_distr[df_distr['District'] == district]['District ID'].values
#     sector_id = df_sector[df_sector['Sector'] == sector]['Sector ID'].values
#     cell_id = df_cell[df_cell['Cell'] == cell]['Cell ID'].values
#     full_name_id = df_name[(df_name['FirstName'] == first_name) & (df_name['LastName'] == last_name)]['FullName ID'].values
#     stock_item_code_id = df_stock_type[df_stock_type['StockItemCode'] == commodity_type]['StockItemCode ID'].values

#     # Return the IDs as a dictionary
#     dict_id = {
#         'Province ID': province_id[0] if province_id.size > 0 else None,
#         'District ID': district_id[0] if district_id.size > 0 else None,
#         'Sector ID': sector_id[0] if sector_id.size > 0 else None,
#         'Cell ID': cell_id[0] if cell_id.size > 0 else None,
#         'FullName ID': full_name_id[0] if full_name_id.size > 0 else None,
#         'StockItemCode ID': stock_item_code_id[0] if stock_item_code_id.size > 0 else None,
#         'Year': year_id,
#         'Month': next_month
#     }
#     id_list = list(dict_id.values())
#     return dict_id

# # Example usage
# # print(collect_ids(
# #     first_name='Mediatrice', last_name='MURORUNKWERE',
# #     province='Kigali', district='Nyarugenge',
# #     sector='Nyarugenge', cell='Kiyovu', commodity_type='RapidDiagnosticTest'
# # ))
