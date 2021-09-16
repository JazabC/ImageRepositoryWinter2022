# ImageRepositoryWinter2022 📸

Created this Image Repository for my Shopify Developer Intern Application! 🗳

## Installation 💻

```bash
pip install pipenv # To install pipenv 
pipenv shell # Spawns a virtual environment
pipenv sync # Installs all dependencies 
```

## Usage For Image Uploading/Deleting Server 

```bash
python mainFlaskServer.py 
```

## How It's Made 
```
Used Flask to create a basic server endpoint
Utilized Firebase for storage 
Fireo as ORM package for Python, specifically for Firebase
```

## Usage For Payment Server 💸

Run following commands within paymentApi directory
```bash
bundle install # Installs all gems
ruby server.rb 
```

## How It's Made 

* Payment Server is not stable yet, included only for demonstrate purposes *
```
Used Ruby Sinatra (DSL for quickly creating web applications in Ruby with minimal effort)
Implemented logic for Stripe API (Payment handling)
Used PaymentIntent method for setting up payments 
```

## Next Steps 💡

* Reduce complexity of certain methods
* Finish payment server 




## License
[MIT](https://choosealicense.com/licenses/mit/)
