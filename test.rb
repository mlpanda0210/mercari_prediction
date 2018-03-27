

require 'json'
require 'httpclient'

input_data = {"main_category":["家電・スマホ・カメラ","家電・スマホ・カメラ"], "sub1_category":["スマホアクセサリー","スマホアクセサリー"],
"sub2_category":["iPhone用ケース","iPhone用ケース"],"price":["100","100"],"brand_name":["ベビーギャップ","ベビーギャップ"],
"ex_item_name":["ルイヴィトン 財布 リメイク 用","ルイヴィトン 財布 リメイク 用"],
"ex_item_description":["韓国 大人気 カカオフレンズ ライアン iPhone 7 ケース 1 ヶ月 使用 綺麗","韓国 大人気 カカオフレンズ ライアン iPhone 7 ケース 1 ヶ月 使用 綺麗"],
"item_condition":["目立った傷や汚れなし","目立った傷や汚れなし"],"shipping_fee":["送料込み","送料込み"]}

json_data = input_data.to_json
post_url = "http://localhost:5000/predict.json/"

client = HTTPClient.new
json = client.post_content(post_url, json_data, "Content-Type" => "application/json")

#uri = URI.parse("http://localhost:5000/predict.json#{params}")
#json = Net::HTTP.get(uri)
result = JSON.parse(json)

p result["result"]
