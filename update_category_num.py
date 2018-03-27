import pandas as pd

def update(df, input_data):
    df = df.fillna("No Data")
    df["Predicted_price"] = df["Predicted_price"].astype('str')
    df["actual_price"] = df["actual_price"].astype('str')
    df = df.to_dict('split')
    del df["index"]
    return df

    # print("update started!!!")
    # output_data = {}
    # for c in input_data:
    #     if c== "すべて":
    #         num = df.shape[0]
    #         output_data[c] = num
    #     else:
    #         output_data[c] = df["main_category"].value_counts()[c]
    # return output_data
