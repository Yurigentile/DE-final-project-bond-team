import pandas as pd
def transform_sales_order(df):
    fact_sales_order = df.copy()
   # fact_sales_order = fact_sales_order.reset_index(level = 1,inplace=True)
    #print(fact_sales_order)



    #Rename column staff_id to sales_staff_id

    fact_sales_order = fact_sales_order.rename(columns = {"staff_id":"sales_staff_id"})
    
    #Create 2 Columns for created_at
    fact_sales_order["created_at"] = pd.to_datetime(fact_sales_order["created_at"])
    fact_sales_order["created_date"] = fact_sales_order["created_at"].dt.date.astype("datetime64[ns]")
    fact_sales_order["created_time"] = fact_sales_order["created_at"].dt.time.astype(str)
    

    #Create 2 Columns for last_updated
    fact_sales_order["last_updated"] = pd.to_datetime(fact_sales_order["last_updated"])
    fact_sales_order["last_updated_date"] = fact_sales_order["last_updated"].dt.date.astype("datetime64[ns]")
    fact_sales_order["last_updated_time"] = fact_sales_order["last_updated"].dt.time.astype(str)
    print(fact_sales_order["last_updated"].dt.time)

    

    #Convert
    fact_sales_order["agreed_payment_date"] = pd.to_datetime(fact_sales_order["agreed_payment_date"])
    fact_sales_order["agreed_payment_date"] = fact_sales_order["agreed_payment_date"].dt.date.astype("datetime64[ns]")

    fact_sales_order["agreed_delivery_date"] = pd.to_datetime(fact_sales_order["agreed_delivery_date"])
    fact_sales_order["agreed_delivery_date"] = fact_sales_order["agreed_delivery_date"].dt.date.astype("datetime64[ns]")
    #Refactoring the index
    fact_sales_order.index = fact_sales_order.index + 1
    fact_sales_order.index.name = "sales_record_id"
    #print(fact_sales_order)
    return fact_sales_order[[
            "sales_order_id",
            "created_date",
            "created_time",
            "last_updated_date",
            "last_updated_time",
            "sales_staff_id",  
            "counterparty_id",
            "units_sold",
            "unit_price",
            "currency_id",
            "design_id",
            "agreed_payment_date",
            "agreed_delivery_date",          
            "agreed_delivery_location_id"]]

