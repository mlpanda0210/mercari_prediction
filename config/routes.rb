Rails.application.routes.draw do
  get '/prediction', to:'predictions#index'
  get '/prediction/prediction', to:'predictions#prediction'
  get '/product/search', to:'products#search'
  get '/product/result', to:'products#result'
  get '/product/update', to:'products#update'
  get '/product', to:'products#index'

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
