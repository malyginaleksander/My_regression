import random

wmeco={"01001": "AGAWAM", "01002": "AMHERST", "01005": "BARRE"}
zip = random.choice(list(wmeco))
city = wmeco.get(zip)
print(zip, city)