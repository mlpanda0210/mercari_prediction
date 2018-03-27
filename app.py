
from flask import Flask, request, render_template, jsonify,json
import pandas as pd
import numpy as np
import sys
from prediction import PredictMercariData
from search import SearchMercariData
from preprocessing import ex_sentence, remove_identifical_word
from scipy.sparse import csr_matrix, hstack
from update_category_num import update

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

def read_csv():
    return pd.read_csv("predicted_item_details.csv")

@app.route('/update_df.json/',methods=['POST'])
def update_df():
    df = read_csv()
    input_data = request.json
    output_data = update(df,input_data)
    return jsonify({'result':str(output_data)})

@app.route('/response_result.json/',methods=['POST'])
def response_result():
    input_data = request.json
    main_category = input_data["main_category"]
    if main_category == "すべて":
        df_selected = df
    else:
        df_selected = df[df["main_category"]==str(main_category)]
    df_selected_dict = df_selected.to_dict()
    return jsonify({'result':str(df_selected_dict)})




# try:
#     df_result = pd.read_csv("predicted_item_details.csv")
#     print("finished to read {} item_details data".format(df_result.shape[0]))
#
# except:
#     print("making item_details data frame")
#     df_result = pd.DataFrame()

# input_data = []
# df = search(input_data)
# df = preprocessing(df)
# df = predict(df)
#
# df_result = pd.concat([df_result,df])
# df_result.to_csv("predicted_item_details.csv" ,index= False)

if __name__ == '__main__':
    app.run()
