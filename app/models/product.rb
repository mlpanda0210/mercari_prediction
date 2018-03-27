class Product < ActiveRecord::Base
  MAIN_CATEGORY = ["すべて","レディース","メンズ","ベビー・キッズ","インテリア・住まい・小物",
    "エンタメ・ホビー","コスメ・香水・美容","家電・スマホ・カメラ","スポーツ・レジャー",
    "ハンドメイド","チケット","自動車・オートバイ","その他"]

    def return_main_category
      return MAIN_CATEGORY
    end

    def save_to_database(hash)
      Product.delete_all

      columns = hash[:columns]
      all_data = hash[:data]
      for data in all_data
        product = Product.new
        i=0
        for column in columns
          product[column] = data[i]
          i = i+1
        end
        product["profit"] =product["actual_price"]-product["Predicted_price"]
        product.save
      end
    end
end
