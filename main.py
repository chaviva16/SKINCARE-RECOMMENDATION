# ---------- main.py ----------
import streamlit as st
import pandas as pd
from preprocess import load_and_clean_data

st.set_page_config(page_title="Skincare Recommender", page_icon="💆‍♀️")
st.title("💆‍♀️ Skincare Product Recommender")
st.markdown("Select your **skin type** and **concern** to find personalized skincare recommendations!")

# Load data
df = load_and_clean_data("data/dermstore_data.json")

# Create dropdowns
all_skin_types = sorted(set([s for lst in df["skin_type"] for s in lst]))
all_skin_concerns = sorted(set([c for lst in df["skin_concern"] for c in lst]))

skin_type = st.sidebar.selectbox("Select your skin type", all_skin_types)
skin_concern = st.sidebar.selectbox("Select your skin concern", all_skin_concerns)

# Filter products
filtered = df[
    df["skin_type"].apply(lambda lst: skin_type in lst) &
    df["skin_concern"].apply(lambda lst: skin_concern in lst)
]

# Toggle to show all results
show_all = st.sidebar.checkbox("Show all results", value=False)

st.subheader(f"Recommended Products for {skin_type} + {skin_concern}")

if not filtered.empty:
    results_to_show = filtered if show_all else filtered.head(5)

    for _, row in results_to_show.iterrows():
        st.markdown("---")
        st.markdown(f"### [{row['title']}]({row['url']})")
        st.markdown(f"**Brand:** {row['brand']}  |  **Price:** ${row['price']}")
        if row["images"]:
            st.image(row["images"].split(",")[0], width=220)
        st.markdown(f"*{row['description'][:300]}...*")

    if not show_all and len(filtered) > 5:
        st.markdown(f"🔎 _{len(filtered) - 5} more results available. Check 'Show all results' to see more._")
else:
    st.warning("No matching products found for this combination.")
