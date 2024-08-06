import os
import pandas as pd

def read_csv_from_file_path(path):
   return pd.read_csv(path)


def get_csvs():
    items_csv_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'Items.csv')
    items_csv_path = os.path.abspath(items_csv_path)
    sales_csv_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'Sales.csv')
    sales_csv_path = os.path.abspath(sales_csv_path)
    return read_csv_from_file_path(items_csv_path),read_csv_from_file_path(sales_csv_path)


if __name__ == "__main__":
    items,sales = get_csvs()
    item_sales = pd.merge(items,sales, on='ItemId',how = 'inner')

    item_sales['SaleDate'] = pd.to_datetime(item_sales['SalesDate'])

    item_sales['TotalCost'] = item_sales['Price'] * item_sales['NumSales']
    ids= items['ItemId'].unique()
    df1 = item_sales.groupby('ItemId').agg(total=('TotalCost', 'sum'),TotalItemsSold=('NumSales', 'sum')).reset_index()
    df1['AvgCost']= df1['total']/df1['TotalItemsSold']
    final_df= df1[['ItemId','AvgCost']]
    final_df.to_csv('output.csv',index=False)

