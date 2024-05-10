import pandas as pd
import overpass

def concat(row: pd.Series):
    values = row[row.notna()].values
    if len(values) == 0:
        return None
    elif len(values) == 1:
        return values[0]
    return "; ".join(values)[:-1]


# fetch all car repair shops located in germany & save them in df
api = overpass.API()
query = f"""
area["ISO3166-1"="DE"][admin_level=2];( node["shop"="mobile_phone"](area);
way["shop"="car_repair"](area);
rel["shop"="car_repair"](area);
);
out center;
"""
response = api.Get(query)
properties = []
for f in response.features:
    properties.append(f["properties"])
df = pd.DataFrame(properties)

# fill null values / concatenate columns that refer to similar properties
# print(list(df.isna().sum().sort_values().index))  # -> get an idea of widely used properties
interesting_columns = {}
interesting_columns["name"] = ["name", "operator", "brand", "brand:wikipedia", "alt_name", "short_name", "name:de", "official_name"]
interesting_columns["website"] = ["website", "contact:website"]
interesting_columns["city"] = ["addr:city", "addr:suburb"]
interesting_columns["street"] = ["addr:street"]
interesting_columns["house_nr"] = ["addr:housenumber", "addr:housename", "entrance", "building", ]
interesting_columns["phone"] = ["phone", "contact:phone", "contact:mobile"]
interesting_columns["postcode"] = ["addr:postcode"]
interesting_columns["email"] = ["email", "contact:email"]
for category in interesting_columns.keys():
    df_category = df[interesting_columns[category]]
    new_col = []
    for _, row in df_category.iterrows():
        new_col.append(concat(row))
    interesting_columns[category] = new_col
df_interesting = pd.DataFrame(interesting_columns)
