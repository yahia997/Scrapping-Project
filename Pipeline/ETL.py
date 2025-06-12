from extract import extract
from Preprocessing import clean
from load import load

# Extract --------------------------------------------------------------------------
cities = ['Alexandria']

data = []
for city in cities:
  inner = extract(city, 10, 0)

  for v in inner:
    data.append(v)

# Transform --------------------------------------------------------------------------
data = clean(data)

# Load --------------------------------------------------------------------------
load(data)