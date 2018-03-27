class ProductsController < ApplicationController
  def index
  end

  def result
    if params["main_category"]["category_name"] == "すべて" then
      @products = Product.all.order(profit: :asc)
    else

      main_category = params["main_category"]["category_name"]
      @products = Product.where(main_category: main_category).order(profit: :asc)
    end

  end

  def update
    input_data = Product.new().return_main_category()
    json_data = input_data.to_json
    post_url = "http://localhost:5000/update_df.json/"

    client = HTTPClient.new
    json = client.post_content(post_url, json_data, "Content-Type" => "application/json")
    result= JSON.parse(json)["result"]
    all_result = eval(result)
    Product.new().save_to_database(all_result)
    redirect_to product_path

  end

  def search
    input_data = {"main_category": params["main_category"]["category_name"]}
    json_data = input_data.to_json
    post_url = "http://localhost:5000/response_result.json/"

    client = HTTPClient.new
    json = client.post_content(post_url, json_data, "Content-Type" => "application/json")

    #uri = URI.parse("http://localhost:5000/predict.json#{params}")
    #json = Net::HTTP.get(uri)
    @result = JSON.parse(json)["result"]
  end
end
