
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder, LabelBinarizer, LabelEncoder,OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split,StratifiedKFold,KFold,train_test_split
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
import pyximport; pyximport.install()
import gc
import time
import lightgbm as lgb
from natto import MeCab

try:
    import cPickle as pickle
except:
    import pickle

from scipy.sparse import csr_matrix, hstack

#1：名詞のみ 2:名詞からさらに限定 3:名詞以外も全部

condition_item_description = 1
condition_item_name = 1


def fill_no_category(df):
    df["category_name"] = df["category_name"].fillna("No_category")
    return df

def fill_no_brand(df):
    df["brand_name"] = df["brand_name"].fillna("No_brand")
    return df

def fill_no_description(df):
    df["item_description"] = df["item_description"].fillna("No_description")
    return df


class Ensemble(object):
    def __init__(self, n_splits, num_base_models,lv):
        self.n_splits = n_splits
        self.num_base_models = num_base_models
        self.lv = lv

    def fit_predict(self, T):

        S_test = np.zeros((T.shape[0], self.num_base_models))
        for i in range(self.num_base_models):

            S_test_i = np.zeros((T.shape[0], self.n_splits))

            for j in range(self.n_splits):
                clf = joblib.load("clf_{}_{}.pkl".format(i,j))
                print("loaded  clf_{}_{}.pkl".format(i,j))
                S_test_i[:, j] = clf.predict(T)

            #test_pred平均をとる
            S_test[:, i] = S_test_i.mean(axis=1)

        S_test = pd.DataFrame(S_test)


        S_test.columns = ["Ridge","Ridge2"]



        return S_test


class PredictMercariData(object):
    def __init__(self,input_data):
        self.input_data = input_data

    def predict(self):
        df=pd.DataFrame(self.input_data)

        initial_time = time.time()
        current_time = time.time()

        df["actual_price"] = df["price"].str.replace(",","").astype(np.int64)
        df = df.drop(["price"],axis=1)
        print("num_df = {}".format(df.shape[0]))

        df = df.reset_index(drop=True)
        df_test=df

        #log
        #y=df["actual_price"]
        y = np.log1p(df["actual_price"])

        df = df.drop(["actual_price"],axis=1)

        lb_brand_name = joblib.load("lb_brand_name.pkl")
        df_brand_name_lb = lb_brand_name.transform(df["brand_name"])


        #category_name
        lb_cn_1 = joblib.load("lb_cn_1.pkl")
        df_cn_1_lb =lb_cn_1.transform(df["main_category"])

        lb_cn_2 = joblib.load("lb_cn_2.pkl")
        df_cn_2_lb =lb_cn_2.transform(df["sub1_category"])

        lb_cn_3 = joblib.load("lb_cn_3.pkl")
        df_cn_3_lb =lb_cn_3.transform(df["sub2_category"])

        #item_description
        if condition_item_description == 1:
            df["ex_item_description_mecab_ipadic_neologd"] = df["ex_item_description_mecab_ipadic_neologd"].fillna("missing")
            t1 =joblib.load("t1.pkl")
            df_description_t =t1.transform(df["ex_item_description_mecab_ipadic_neologd"])

        elif condition_item_description == 2:
            df["ex_item_description_selected"] = df["ex_item_description_selected"].fillna("missing")
            df_description_t =t1.transform(df["ex_item_description_selected"])

        elif condition_item_description == 3:
            df["ex_item_description_all"] = df["ex_item_description_all"].fillna("missing")
            df_description_t =t1.transform(df["ex_item_description_all"])

        #name
        if condition_item_name == 1:
            df["ex_item_name_mecab_ipadic_neologd"] = df["ex_item_name_mecab_ipadic_neologd"].fillna("missing")
            t2 = joblib.load("t2.pkl")
            df_name_t =t2.transform(df["ex_item_name_mecab_ipadic_neologd"])

        elif condition_item_name == 2:
            df["ex_item_name_selected"] = df["ex_item_name_selected"].fillna("missing")
            t2 =TfidfVectorizer(use_idf=True, max_features=NUM_name,token_pattern=u'(?u)\\b\\w+\\b')
            df_name_t =t2.transform(df["ex_item_name_selected"])

        elif condition_item_name == 3:
            df["ex_item_name_all"] = df["ex_item_name_all"].fillna("missing")
            t2 =TfidfVectorizer(use_idf=True, max_features=NUM_name,token_pattern=u'(?u)\\b\\w+\\b')
            df_name_t =t2.transform(df["ex_item_name_all"])

        #item_condition_id
        lb_item_condition = joblib.load("lb_item_condition.pkl")
        df_ici_csr = lb_item_condition.transform(df["item_condition"])
        print("lb_item_condition loaded")

        #shipping
        lb_shipping_fee = joblib.load("lb_shipping_fee.pkl")
        df_s_csr = lb_shipping_fee.transform(df["shipping_fee"])
        print("lb_shipping_fee loaded")


        merge_matrix = hstack([df_brand_name_lb,df_cn_1_lb,df_cn_2_lb,df_cn_3_lb,df_description_t,df_name_t,df_ici_csr,df_s_csr]).tocsr()

        X_merge_test = merge_matrix

        #モデル構築
        X_test = X_merge_test
        stack1 = Ensemble(n_splits=3,num_base_models = 2,lv=1)
        s1_test = stack1.fit_predict(X_test)

        #Ridgeの結果を元のデータとマージ
        X_test = hstack([X_test,s1_test])

        with open('gbm_0.pkl', 'rb') as gbm_0:
            model1 = pickle.load(gbm_0)

        model1 = lgb.Booster(model_file='gbm_0.txt')
        predsL = model1.predict(X_test)



        with open('gbm_1.pkl', 'rb') as gbm_1:
            model2 = pickle.load(gbm_1)

        model2 = lgb.Booster(model_file='gbm_1.txt')
        predsL2 = model2.predict(X_test)

        #予測

        y_pred =0.5* predsL + 0.5*predsL2
        y_pred_expm1 = np.expm1(y_pred).astype(np.int32)
        df_predicted = pd.DataFrame(y_pred_expm1,index=df_test.index,columns=["Predicted_price"])

        df_test_result = pd.concat([df_predicted,df_test],axis=1)
        df_test_result.loc[df_test_result['Predicted_price']<=0, "Predicted_price"] =0.0
        return df_test_result
