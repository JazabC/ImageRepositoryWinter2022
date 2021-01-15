# ImageRepositorySpring2021

Created this Image Repository for my Shopify Developer Intern Application!
`bash:camera:`

## Installation

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

## Usage For Payment Server

```bash
bundle install # Installs all gems
ruby server.rb
```

## How It's Made 
```
Used Ruby Sinatra (DSL for quickly creating web applications in Ruby with minimal effort)
Implemented logic for Stripe API (Payment handling)
Used PaymentIntent method for setting up payments 
* Payment Server is not stable yet but I wanted to include it to demonstrate the progress *
```



## License
[MIT](https://choosealicense.com/licenses/mit/)
