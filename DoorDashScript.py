import pandas as pd

df = pd.read_csv('consumer_order_details.csv',parse_dates=['CREATED_AT', 'DELIVERY_TIME'], encoding='utf-8')

def make_trip_id(row):
    import pandas as pd
    import hashlib
    key = f"{row['STORE_NAME']}|{row['CREATED_AT']}|{row['DELIVERY_ADDRESS']}"
    return hashlib.md5(key.encode()).hexdigest()

df["trip_id"] = df.apply(make_trip_id, axis=1)

item_clean_map = {
    'grilled cheese': 'Grilled Cheese',
    'spanakopita': 'Spinach Pie',
    'spinach pie': 'Spinach Pie',
    'eggplant caprese': 'Eggplant Caprese',
    'dry fried soman': 'Dry Fried Soman',
    'pad thai': 'Pad Thai',
    'red curry': 'Red Curry',
    'green curry': 'Green Curry',
    'gaeng keow wan': 'Green Curry',
    'keemao': 'Drunken Noodle',
    'kea mow': 'Drunken Noodle',
    'drunken noodle': 'Drunken Noodle',
    'hash and eggs': 'Hash & Eggs',
    'birria quesadilla': 'Birria Quesadilla',
    'empanada': 'Empanada',
    'eggplant parm': 'Eggplant Parmesan',
    'rollatini': 'Eggplant Parmesan',
    'mac & cheese': 'Mac and Cheese',
    'macaroni': 'Mac and Cheese',
    'sweet potato roll': 'Sweet Potato Sushi Roll',
    'the spicy mike': 'The Spicy Mike',
    'the nikki newark': 'The Nikki Newark'
}


def normalize_item(text):
    import re
    text = str(text).lower()

    # remove encoding junk
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # remove leading numbers / symbols
    text = re.sub(r'^[#*\d\s./()-]+', '', text)

    # remove sizes & quantities
    text = re.sub(
        r'(\b\d+\/\d+\b|\b\d+\s*(oz|pcs|pieces|piece|inch|")\b|\([^)]*\))',
        '',
        text
    )

    # normalize punctuation
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def resolve_item(item):
    item_lower = item.lower()

    # utensils / flatware
    if any(x in item_lower for x in ['utensil', 'flatware', 'cutlery', 'napkin']):
        return 'Utensils'

    # keyword-based canonical mapping
    for key, value in item_clean_map.items():
        if key in item_lower:
            return value

    # fallback: title-case cleaned text
    return item.title()

df['ITEM_CLEANED'] = (
    df['ITEM']
    .apply(normalize_item)
    .apply(resolve_item)
)


cleanup_map = {
    'Seasonal Specials': 'Seasonal Specials',
    'Specials': 'Seasonal Specials',
    'ALL DAY BREAKFAST': 'Breakfast',
    'Breakfast Burritos': 'Breakfast',
    'Breakfast': 'Breakfast',
    'Sandwich': 'Sandwiches/Paninis/Wraps',
    'Specialty Sandwiches': 'Sandwiches/Paninis/Wraps',
    'Hot Sandwiches': 'Sandwiches/Paninis/Wraps',
    'Focaccia Sandwiches (Housemade Bread Specials)': 'Sandwiches/Paninis/Wraps',
    'Cold Subs': 'Sandwiches/Paninis/Wraps',
    'Panini': 'Sandwiches/Paninis/Wraps',
    'WRAPS': 'Sandwiches/Paninis/Wraps',
    'Wraps': 'Sandwiches/Paninis/Wraps',
    'Salads': 'Salads & Bowls',
    'Salads & Bowls': 'Salads & Bowls',
    'Bowls + Trays': 'Salads & Bowls',
    'Soups': 'Soups & Sides',
    'Soups & Mac': 'Soups & Sides',
    'Sides': 'Soups & Sides',
    'Small Plates': 'Appetizers & Small Plates',
    'Appetizers': 'Appetizers & Small Plates',
    'Entrees From the Grill': 'Entrees / Mains',
    'Mains': 'Entrees / Mains',
    'Grill': 'Grill & Meats',
    'Pizza': 'Pizza & Flatbreads',
    'Flatbreads': 'Pizza & Flatbreads',
    'Cauliflower Pies': 'Pizza & Flatbreads',
    'Tacos': 'Mexican',
    'Enchiladas': 'Mexican',
    'Burritos': 'Mexican',
    'Quesadillas': 'Mexican',
    'Goops+Scoops': 'Desserts',
    'Desserts': 'Desserts',
    'Kids menu': 'Kids / Family',
    'taco packs': 'Mexican',
    'Extras': 'Extras / Condiments',
    'Shared Sides': 'Extras / Condiments',
    'Sauces': 'Extras / Condiments',
    '#NAME?': 'Unknown / Misc',
    'Empanadas':'Mexican',
    'The Don Gregorio':'Pizza & Flatbreads',
    'Crispy Brussels Sprouts':'Soups & Sides',
    'Chicago Style':'Sandwiches/Paninis/Wraps',
    'Green Curry':'Thai',
    'The Nikki Newark':'Sandwiches/Paninis/Wraps',
    'Caprino':'Pizza & Flatbreads',
    'The Spicy Mike':'Sandwiches/Paninis/Wraps',
    'The Titan':'Sandwiches/Paninis/Wraps',
    'ATAVIROS':'Sandwiches/Paninis/Wraps',
    'üî•Thai Green Curry Lunch':'Thai',
    'The Nikki Newark':'Sandwiches/Paninis/Wraps',
    'EGGPLANT CAPRESE PANINI':'Sandwiches/Paninis/Wraps',
    'Wise Guy Eggppant Focaccia':'Pizza & Flatbreads',
    'Large 16" Grandma Pie':'Pizza & Flatbreads',
    'Large 16" Grandma Pie':'Pizza & Flatbreads',
    'Green Curry':'Thai',
    'Drunken Noodle':'Thai',
    'Keemao Noodle':'Thai',
    'Keemao Noodle':'Thai',
    '20 Oz. Sodas':'Drinks',
    'Water kirkland bottle':'Drinks',
    'Crispy Goat Cheese':'Salads & Bowls',
    'Thirty Acres':'Salads & Bowls',
    'Meatball & Cheese Sandwich':'Sandwiches/Paninis/Wraps',
    'BB Potato Chorizo':'Breakfast',
    'Gyro':'Sandwiches/Paninis/Wraps',
    'Enlightened Mediterranean Chicken Pita Tacos':'Mexican',
    'Hash and Eggs':'Breakfast',
    'Jersey Devil':'Breakfast',
    'Stack':'Mexican',
    'Homewrecker Bowl':'Mexican',
    'The Uptown':'Sandwiches/Paninis/Wraps',
    'Breaded Eggplant Wrap':'Sandwiches/Paninis/Wraps',
    'Honey Sriracha Brussels Sprouts':'Soups & Sides',
    '10" Salsiccia':'Pizza & Flatbreads',
    'Cauliflower Bites':'Soups & Sides',
    'El Diablo':'Mexican',
    'Chorizo Mix Potato Pambazotradicional':'Mexican',
    None: 'Unknown / Misc'
}


df['CATEGORY_CLEANED'] = df['ITEM_CLEANED'].map(cleanup_map)

# Fallback to CATEGORY if ITEM_CLEANED didn't match
df['CATEGORY_CLEANED'] = df['CATEGORY_CLEANED'].fillna(df['CATEGORY'].map(cleanup_map))

# Final fallback
df['CATEGORY_CLEANED'] = df['CATEGORY_CLEANED'].fillna('Unknown / Misc')

def infer_category_from_item(item):
    key = str(item).lower()
    if any(word in key for word in ['grilled cheese', 'the italian', 'hot dog', 'burger', 'gyro', 'sandwich', 'dog', 'club', 'wrap', 'pita', 'panini', 'blt', 'frisky whiskey', 'the cuban', 'the jersey city', 'greek eltdown','falafel']):
        return "Sandwiches/Paninis/Wraps"
    elif any(word in key for word in ["enchilada", "taco", "burrito", "sope", "quesabir", "chiles", "quesadilla", "tacos", 'pollo', 'nachos', 'mexican', 'stack', 'puebla', 'tamal', 'mexico', 'empanadas', 'guacamole', "moe's famous queso",'salsa']):
        return "Mexican"
    elif any(word in key for word in ["pasta", "lasagna", "gnocchi", "cavatelli", "vodka", "fontina", 'rigatoni', 'vitello milanese', 'eggplant parmesan', 'chicken parmesan', 'tortellini']):
        return "Italian"
    elif any(word in key for word in ["salad", "bowl", 'crispy goat cheese']):
        return "Salads & Bowls"
    elif any(word in key for word in ['tender', 'tenders', 'wings', 'mozzarella sticks']):
        return "Appetizers & Small Plates"
    elif any(word in key for word in ['personal pie', 'flatbread', 'pizza', 'personal', 'margheroni']):
        return "Pizza & Flatbreads"
    elif any(word in key for word in ["platter", "sausage", "ribs", "brisket", "chicken", "gyro platter", "burnt ends", "stew", "bbq", 'pulled pork']):
        return "BBQ"
    elif any(word in key for word in ["fries", "rings", "tots", "chips", "plantain", "cassava", "pierog", "dip", 'brussel sprouts', 'french onion', 'puppies', 'hummus', 'mac & cheese', 'collard greens']):
        return "Soups & Sides"
    elif "soup" in key or "chili" in key:
        return "Soups & Sides"
    elif "baklava" in key or "dessert" in key:
        return "Desserts"
    elif "sauce" in key or "utensils" in key or "napkins" in key:
        return "Extras / Condiments"
    elif key.strip() in ["soda", "beer", "juice"]:
        return "Beverages"
    elif any(word in key for word in ["hibachi", 'california roll']):
        return "Japanese"
    elif any(word in key for word in ["general tso", 'dumpling']):
        return "Chinese"
    elif any(word in key for word in ["thai", "drunken noodle", 'pad thai']):
        return "Thai"
    elif any(word in key for word in ['naan', 'samosa', 'kofta', 'pakora', 'gosht']):
        return "Indian"
    elif any(word in key for word in ["toast", 'hash and eggs', 'mr. potato head']):
        return "Breakfast"
    else:
        return "Unknown / Misc"

# Apply only to rows where category is unknown
mask_unknown = df['CATEGORY_CLEANED'] == 'Unknown / Misc'
df.loc[mask_unknown, 'CATEGORY_CLEANED'] = df.loc[mask_unknown, 'ITEM_CLEANED'].apply(infer_category_from_item)


# Date Parse
df['DELIVERY_TIME'] = pd.to_datetime(df['DELIVERY_TIME'], errors='coerce')
df['hour_minute_CREATED_AT'] = df['CREATED_AT'].dt.strftime('%I:%M %p')
df['hour_minute_DELIVERY_TIME'] = df['DELIVERY_TIME'].dt.strftime('%I:%M %p')
df["DELIVERY_LENGTH"] = (df['DELIVERY_TIME'] - df['CREATED_AT'])
df['am_pm_flag'] = df['hour_minute_CREATED_AT'].apply(lambda x: 'PM' if 'PM' in x else 'AM')


def add_meal_period(df, order_time_col="CREATED_AT"):

    hours = df[order_time_col].dt.hour

    df["Meal Type"] = pd.cut(
        hours,
        bins=[-1, 4, 10, 14, 16, 21, 23],
        labels=[
            "Late Night",
            "Breakfast",
            "Lunch",
            "Afternoon",
            "Dinner",
            "Late Night",
        ],
        ordered=False
    )

    return df

df = add_meal_period(df)

def normalize_text(s):
    import unicodedata
    import re
    if pd.isna(s):
        return s

    s = str(s)

    # --- Fix known mojibake first ---
    s = s.replace("Â®", "")
    s = s.replace("â€™", "'")

    # --- Normalize all apostrophe variants ---
    s = s.replace("’", "'")
    s = s.replace("‘", "'")
    s = s.replace("`", "'")

    # --- Unicode normalize & ASCII clean ---
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")

    # --- Cleanup ---
    s = " ".join(s.split())
    return s.strip()



def clean_column_unicode(df, column):
    df = df.copy()

    df[column] = (
        df[column]
        .apply(normalize_text) 
        .str.strip()
    )

    return df

def geocode_address(address, max_attempts=3):
    import pandas as pd
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError

    geolocator = Nominatim(user_agent="door-dash-wrapped-analyzer")

    if pd.isna(address) or address == "":
        return None, None
    
    # 1. List of addresses to try, from most to least specific
    addresses_to_try = [
        address, 
        # Remove "USA" and extra details
        address.replace(", USA", "").replace(".", ""),
        # Simplified: Just street, city, state, ZIP
        ', '.join(address.split(', ')[:4]) 
    ]
    if address:
        address = address.replace(" Rte ", " Route ")
        address = address.replace(" Ave", " Avenue")
        address = address.replace(" Rd", " Road")
        address = address.replace(" Dr", " Drive")
        address = address.replace(" Brg", " Bridge")
        # You might also want to ensure "USA" is appended if it's missing
        if not address.strip().endswith("USA"):
            address = f"{address}, USA"
    
    # Use a set to avoid trying the same address twice
    for addr_to_try in set(addresses_to_try):
        for attempt in range(max_attempts):
            try:
                location = geolocator.geocode(addr_to_try, timeout=10)
                
                if location:
                    return location.latitude, location.longitude
                
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                # You can add a short sleep here if needed, but let's prioritize trying the next address
                pass # Continue to the next attempt or next address
    
    # If all attempts failed
    return None, None

def get_total_cost(df):
    df["EST_FEES"] = df["SUBTOTAL"] * 0.13
    df["EST_TAX"] = (df["SUBTOTAL"] + df["EST_FEES"]) * 0.08
    df["EST_TIP"] = (df["SUBTOTAL"] + df["EST_TAX"] + df["EST_FEES"]) * 0.10
    df["EST_TOTAL"] = (df["SUBTOTAL"] + df["EST_TAX"] + df["EST_FEES"] + df["EST_TIP"])

    return df

df= get_total_cost(df)

# def get_RestaurantAddress(df):
#     addy = pd.read_excel('DoorDashRestaurantAddressLookup.xlsx')

#     df = clean_column_unicode(df, 'STORE_NAME')
#     addy = clean_column_unicode(addy, 'STORE_NAME')

#     addy[['delivery_lat', 'delivery_long']] = addy.apply(
#     lambda row: geocode_address(row['DELIVERY_ADDRESS']), 
#     axis=1, 
#     result_type='expand')

#     addy[['resturant_lat', 'resturant_long']] = addy.apply(
#         lambda row: geocode_address(row['Restaurant Address']), 
#         axis=1, 
#         result_type='expand')

#     return pd.merge(df, addy, on=['STORE_NAME','DELIVERY_ADDRESS'], how='left')

# df = get_RestaurantAddress(df)

def unwrapped_me():
    # =========================
    # DoorDash Unwrapped Summary
    # =========================
    import csv

    summary = {}
    

    summary["total_orders"] = df["trip_id"].nunique()
    summary["total_items_ordered"] = len(df)
    summary["unique_restaurants"] = df["STORE_NAME"].nunique()

    # Favorites
    summary["favorite_restaurant"] = (
        df["STORE_NAME"].value_counts().idxmax()
    )

    summary["favorite_item"] = (
        df["ITEM_CLEANED"].value_counts().idxmax()
    )

    summary["top_category"] = (
        df["CATEGORY_CLEANED"].value_counts().idxmax()
    )

    summary["peak_meal"] = (
        df["Meal Type"].value_counts().idxmax()
    )

    # Spend (item-level safe)
    summary["est_total_spent"] = df["EST_TOTAL"].sum()

    # Order-level spend calculations
    order_totals = df.groupby("trip_id")["EST_TOTAL"].sum()

    summary["avg_order_spend"] = order_totals.mean()
    summary["largest_order"] = order_totals.max()
    summary["smallest_order"] = order_totals.min()

    # Restaurant spend behavior
    summary["most_spent_restaurant"] = (
        df.groupby("STORE_NAME")["EST_TOTAL"].sum().idxmax()
    )

    summary["most_spent_restaurant_amount"] = (
        df.groupby("STORE_NAME")["EST_TOTAL"].sum().max()
    )

    # Ordering habits
    summary["avg_items_per_order"] = (
        df.groupby("trip_id").size().mean()
    )

    summary["max_items_in_single_order"] = (
        df.groupby("trip_id").size().max()
    )

    # Delivery time insights (if available)
    summary["avg_delivery_minutes"] = (
        df["DELIVERY_LENGTH"].dt.total_seconds().mean() / 60
    )

    summary["fastest_delivery_minutes"] = (
        df["DELIVERY_LENGTH"].dt.total_seconds().min() / 60
    )

    summary["slowest_delivery_minutes"] = (
        df["DELIVERY_LENGTH"].dt.total_seconds().max() / 60
    )

    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(
    "unwrapped_summary.csv", 
    sep='\t',        # 👈 Use Tab instead of Comma
    index=False, 
    encoding='utf-8-sig' # 👈 Adds BOM to help Excel/Browsers recognize UTF-8
)

    # Chart data
    df["month"] = df["CREATED_AT"].dt.to_period("M").astype(str)
    orders_by_month = (
    df.drop_duplicates("trip_id")
      .assign(
          month=df["CREATED_AT"].dt.to_period("M").astype(str),
          month_name=df["CREATED_AT"].dt.month_name()
      )
      .groupby(["month", "month_name"], as_index=False)
      .size()
      .rename(columns={"size": "count"})
      .sort_values("month")
    )
    
    df["CATEGORY_CLEANED"].value_counts().to_csv("category_counts.csv")
    df["ITEM_CLEANED"].value_counts().head(10).to_csv("top_items.csv")
    df["STORE_NAME"].value_counts().head(10).to_csv("top_places.csv")
    df["Meal Type"].value_counts().to_csv("meal_type_counts.csv")
    orders_by_month.to_csv("orders_by_month.csv", index=False)

    print("🎁 Unwrapped data exported!")

unwrapped_me()


df.to_csv('VisualizeData.csv', index=False)
print("✅ Run Complete! Data saved to 'VisualizeData.csv'")