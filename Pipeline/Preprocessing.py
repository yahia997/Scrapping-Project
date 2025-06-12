# this code is written by Hamed
from datetime import datetime
import re

# cities list
cities = [
  'Alexandria',
  'Cairo',
  'Hurghada',
  'Sharm El Sheikh',
  'Ain Sokhna',
  'Dahab',
  'Port Said',
  'North Coast',
  'Fayoum',
  'Aswan',
  'Marsa Alam',
  'Ismailia',
]

# function to clean each object
def preprocess_hotel(hotel):
    # separate longitude and latitude with regex
    lat_long = re.findall(r"[-+]?\d*\.\d+|\d+", hotel.get("address", ""))
    hotel["latitude"] = float(lat_long[0]) if len(lat_long) > 0 else None
    hotel["longitude"] = float(lat_long[1]) if len(lat_long) > 1 else None
    hotel.pop("address") # removing old atrribute

    # get city and country from address
    address2 = hotel.get("address2", "")

    # if address contains city in our cities we choose it
    for city in cities:
        if address2.find(city) != -1:
            hotel["city"] = city
            break

    hotel["country"] = "Egypt" # country is always egypt
    # removing all text after the country (not wanted part)
    address_cleaned = re.sub(r"(.+)Egypt(.+)", r"\1Egypt", address2)
    hotel["address"] = address_cleaned
    hotel.pop("address2") # remove old field

    # extract the number from reviews_cnt
    reviews_cnt = hotel.get("reviews_cnt", "")
    reviews = re.findall(r"[0-9,]+", reviews_cnt)
    reviews_comma_removed = re.sub(r",", "", reviews[0] if len(reviews) > 0 else "")
    hotel["reviews_cnt"] = int(reviews_comma_removed) if reviews else 0

    # extract the number from rating
    rating = hotel.get("rating", "")
    rate_val = re.findall(r"\d+\.?\d*", rating)
    hotel["rating"] = float(rate_val[0]) if rate_val else None

    # the same for rating details
    if "rating_details" in hotel:
     updated_details = {}
    for k, v in hotel["rating_details"].items():
        val = re.findall(r"\d+\.?\d*", v)
        updated_details[k.strip()] = float(val[0]) if val else None
    hotel["rating_details"] = updated_details

    # fixing comments
    cleaned_comments = []
    for comment in hotel.get("comments", []):
        name = comment.get("name", "")
        desc_split = re.split(r"[“”\"]", name)
        if len(desc_split) > 1:
            comment["name"] = desc_split[0].split(" ")[0]
            comment["description"] = desc_split[1]
        else:
            comment["description"] = comment.get("description", "")

        cleaned_comments.append({
            "name": comment.get("name", "").strip(),
            "country": comment.get("country", "").strip(),
            "description": comment.get("description", "").strip()
        })
    hotel["comments"] = cleaned_comments
    # we can do it also with maps


    # removing duplicates from facilities
    hotel["facilities"] = list(set(hotel.get("facilities", [])))


    # removing extra <h2></h2> in description
    description = hotel.get("description", "")
    description = re.sub(r"<\/?h2>", "", description)
    description = ' '.join(description.split())
    hotel["description"] = description

    # extracting number from price
    price = hotel.get("price", "")
    if price == "Unkown":
        hotel["price"] = None
    else:
        price_val = re.findall(r"[0-9,]+", price)
        price_comma_removed = re.sub(r",", "", price_val[0])
        hotel["price"] = float(price_comma_removed)
    
    hotel['date'] = datetime.now()

    return hotel


# function to clean
def clean(data):
    cleaned_data = []
    seen_hotels = set()
    
    # go through each object in the list
    for hotel in data:
        # check duplicates
        if hotel["title"] in seen_hotels:
            continue
        seen_hotels.add(hotel["title"])
        
        cleaned_hotel = preprocess_hotel(hotel)
        cleaned_data.append(cleaned_hotel)

    return cleaned_data