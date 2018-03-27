class CreateProducts < ActiveRecord::Migration[5.0]
  def change
    create_table :products do |t|
      t.integer :Predicted_price
      t.integer :actual_price
      t.string :item_description
      t.string :item_condition
      t.string :item_name
      t.string :main_category
      t.string :brand_name
      t.string :shipping_fee
      t.string :sold_badge
      t.string :sub1_category
      t.string :sub2_category
      t.string :ex_item_name_mecab_ipadic_neologd
      t.string :ex_item_description_mecab_ipadic_neologd

      t.string :url
      t.string :pic
      t.integer :profit


    end
  end
end
