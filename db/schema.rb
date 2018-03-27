# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20180211115906) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "products", force: :cascade do |t|
    t.integer "Predicted_price"
    t.integer "actual_price"
    t.string  "item_description"
    t.string  "item_condition"
    t.string  "item_name"
    t.string  "main_category"
    t.string  "brand_name"
    t.string  "shipping_fee"
    t.string  "sold_badge"
    t.string  "sub1_category"
    t.string  "sub2_category"
    t.string  "ex_item_name_mecab_ipadic_neologd"
    t.string  "ex_item_description_mecab_ipadic_neologd"
    t.string  "url"
    t.string  "pic"
    t.integer "profit"
  end

end
