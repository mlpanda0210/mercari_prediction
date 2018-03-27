import pandas as pd
import numpy as np
import sys
from prediction import PredictMercariData
from search import SearchMercariData
from preprocessing import ex_sentence, remove_identifical_word, ex_sentence_mecab_ipadic_neologd
from scipy.sparse import csr_matrix, hstack
from update_category_num import update

def preprocessing(df):
    df["ex_item_name_mecab_ipadic_neologd"] = df["item_name"].apply(lambda x: ex_sentence_mecab_ipadic_neologd(x))
    df["ex_item_name_mecab_ipadic_neologd"] = df["ex_item_name_mecab_ipadic_neologd"].apply(lambda x: remove_identifical_word(x))
    print("item_name finised")
    df["ex_item_description_mecab_ipadic_neologd"] = df["item_description"].apply(lambda x: ex_sentence_mecab_ipadic_neologd(x))
    df["ex_item_description_mecab_ipadic_neologd"] = df["ex_item_description_mecab_ipadic_neologd"].apply(lambda x: remove_identifical_word(x))
    print("ex_item_description_mecab_ipadic_neologd")
    return df


def predict(df):
    print("predict started")
    input_data = df
    model = PredictMercariData(input_data)
    price = model.predict()
    return price

def search(input_data):
    print("search started")
    input_data = input_data
    model = SearchMercariData(input_data)
    df = model.search_from_sold_list()
    return df

try:
    df_result = pd.read_csv("predicted_item_details.csv")
    print("finished to read {} item_details data".format(df_result.shape[0]))

except:
    print("making item_details data frame")
    df_result = pd.DataFrame()

input_data = []
df = search(input_data)
df = preprocessing(df)
df = predict(df)

df_result = pd.concat([df_result,df])
df_result.to_csv("predicted_item_details.csv" ,index= False)
