# Payment server code
require "google/cloud/firestore"
require 'sinatra'
require 'stripe'

Stripe.api_key = 'sk_test_51I79EYIusRttpMpYOCTcYHEi37L6LVwUrFtOLSIJ8cgOLqXfVk1zXgB4v9UvGE98jhw7EII752BKZeUP27d578jM00VfNLAuuD'

set :static, true
set :public_folder, File.join(File.dirname(__FILE__), '.')
set :port, 4242
# initialize firestore connection
db = Google::Cloud::Firestore.new(
  project_id: 'shopifyimagerepoproject',
  credentials: "/Users/jazab/Desktop/ShopifyChallengeByJazab/paymentAPI/shopify-challenge-jazab-key.json"
) 

def calculate_order_amount(imageId)
  # # Get a collection reference
  # cities_col = firestore.col "ImagesCollection"

  # # Get a document reference
  # nyc_ref = cities_col.doc "#{imageId}"

  # # The document ID is what was provided
  # puts nyc_ref.productPrice #=> "NYC"
123



  # doc_ref  = db.doc "#{ImagesCollection}/#{imageId}"
  # snapshot = doc_ref.get
  # if snapshot.exists?
  #   puts "#{snapshot.document_id} data: #{snapshot.data.productPrice}."
  # else
  #   puts "Document #{snapshot.document_id} does not exist!"
end


# An endpoint to start the payment process
post '/create-payment-intent' do
  content_type 'application/json'
  data = JSON.parse(request.body.read)

  # Create a PaymentIntent with amount and currency
  payment_intent = Stripe::PaymentIntent.create(
    amount: calculate_order_amount(data['imageId']),
    currency: 'usd'
  )
  
  {
    clientSecret: payment_intent['client_secret'],
  }.to_json
end
