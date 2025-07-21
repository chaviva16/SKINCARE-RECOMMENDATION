# ---------- preprocess.py ----------
import json
import pandas as pd
import re

# Define valid types and concerns to filter noise
VALID_SKIN_TYPES = {
    "Oily Skin", "Dry Skin", "Normal Skin",
    "Sensitive Skin", "Mature Skin", "Acne-Prone Skin"
}

VALID_SKIN_CONCERNS = {
    "Acne", "Dark Spots", "Redness", "Large Pores",
    "Loss of Firmness", "Aging", "Uneven Skin Tone"
}

def parse_skin_info(value):
    if not value or not isinstance(value, str):
        return [], []

    concerns = set()
    skin_types = set()

    chunks = re.split(r'[,\n]', value)
    for chunk in chunks:
        chunk = chunk.strip()
        for t in VALID_SKIN_TYPES:
            if t.lower() in chunk.lower():
                skin_types.add(t)
        for c in VALID_SKIN_CONCERNS:
            if c.lower() in chunk.lower():
                concerns.add(c)

    return list(skin_types), list(concerns)

def load_and_clean_data(path):
    with open(path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    df = pd.DataFrame(raw_data)
    df = df[["title", "brand", "price", "description", "images", "url", "skin_type_and_concerns"]]
    df.dropna(subset=["title", "brand", "price"], inplace=True)
    df["price"] = df["price"].astype(float)
    df["skin_type"], df["skin_concern"] = zip(*df["skin_type_and_concerns"].apply(parse_skin_info))

    return df
