import requests
ProductSlug='0820dm_winback_75_bonus'
State='nj'.lower()
UtilitySlug='ace'

query_text ='http://products.pt.nrgpl.us/api/v1/products/?channel=web&product_slug='+ProductSlug+'&state_slug='+State+"&utility_slug="+UtilitySlug
response = requests.get(query_text)
data = response.json()



print(data['results'][0]['sku'])