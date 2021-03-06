import pandas as pd
from visualize_result import *
def process_excel(df):
    df.to_excel("Amazon.xlsx", index=False)
    df['Order Date'] = pd.to_datetime(df['Order Date'])

    df.loc[df["Order Type"].str.contains("Delivered|Dispatched|Replace"), "Order Type"] = "Product"
    df.loc[df["Order Type"].str.contains("Return|Refund"), "Order Type"] = "Order returned"
    df.loc[df["Order Type"].str.contains("Successful"), "Order Type"] = "Bill"
    df['Order Year'] = pd.DatetimeIndex(df['Order Date']).year
    df_filtered = df[(df["Order Type"] != 'Order returned')]

    df2=df_filtered
    df2 = df2.groupby('Order Year').sum()
    df2['Order Year'] = df2.index
    df.to_excel("Amazon.xlsx", index=False)
    df['Order Value'] = abs(df['Order Value'])
    show_graph(df_filtered,df2)
