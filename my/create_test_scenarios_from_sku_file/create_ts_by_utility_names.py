

brand = "Cirro"
channel = 'web'
test_name = brand + str("_web_regression")
environment = 'pt'
url_api= 'http://products.'+environment+'.nrgpl.us/api/v1/products/'


parametrs ={
    'brand_slug':brand.lower(),
    'channel': channel,
    'status':'published',
    }
