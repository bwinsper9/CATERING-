import streamlit as st
import pandas as pd
import base64

def scale_recipe(ingredients_for_10, number_of_guests):
    scaled_ingredients = {}
    scale_factor = number_of_guests / 10
    for ingredient, (quantity, ing_type) in ingredients_for_10.items():
        scaled_ingredients[ingredient] = (quantity * scale_factor, ing_type)
    return scaled_ingredients

def generate_shopping_list(scaled_ingredients):
    retail_list = "Retail Ingredients:\n"
    wholesale_list = "Wholesale Ingredients:\n"

    for ingredient, (quantity, ing_type) in scaled_ingredients.items():
        if ing_type == 'retail':
            retail_list += f"- {ingredient}: {quantity:.2f}\n"
        elif ing_type == 'wholesale':
            wholesale_list += f"- {ingredient}: {quantity:.2f}\n"

    return f"{retail_list}\n{wholesale_list}"

def generate_recipe(scaled_ingredients):
    recipe = "Recipe Instructions:\n"
    recipe += "1. Prepare all ingredients as listed.\n"
    recipe += "2. Combine and cook as per your standard method or recipe instructions.\n"
    recipe += "\nIngredients Needed:\n"
    for ingredient, (quantity, _) in scaled_ingredients.items():
        recipe += f"- {ingredient}: {quantity:.2f}\n"
    return recipe

def load_ingredients_from_file(uploaded_file):
    df = pd.read_csv(uploaded_file)
    ingredients = {}
    for index, row in df.iterrows():
        ingredients[row['Ingredient']] = (row['Quantity'], row['Type'])
    return ingredients

def generate_csv_download_link(csv_content, filename):
    b64 = base64.b64encode(csv_content.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download Sample CSV</a>'
    return href

# Streamlit App
st.title("Catering Recipe Scaler")

st.header("Upload or Manually Input Your Ingredients")
option = st.radio("Choose Input Method:", ("Upload CSV", "Manual Input"))

ingredients_for_10 = {}

if option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file with columns: Ingredient, Quantity, Type", type=["csv"])
    if uploaded_file:
        ingredients_for_10 = load_ingredients_from_file(uploaded_file)

elif option == "Manual Input":
    num_ingredients = st.number_input("Number of Ingredients", min_value=1, value=5)
    for i in range(int(num_ingredients)):
        ingredient = st.text_input(f"Ingredient {i+1} Name")
        quantity = st.number_input(f"Ingredient {i+1} Quantity", min_value=0.0, value=0.0)
        ing_type = st.selectbox(f"Ingredient {i+1} Type", ("wholesale", "retail"))
        if ingredient:
            ingredients_for_10[ingredient] = (quantity, ing_type)

st.header("Enter Number of Guests")
number_of_guests = st.number_input("Number of Guests", min_value=1, value=10)

if st.button("Generate Shopping List and Recipe") and ingredients_for_10:
    scaled_ingredients = scale_recipe(ingredients_for_10, number_of_guests)
    shopping_list = generate_shopping_list(scaled_ingredients)
    recipe = generate_recipe(scaled_ingredients)
    st.text_area("Shopping List", shopping_list, height=300)
    st.text_area("Generated Recipe", recipe, height=400)

st.markdown("---")
st.markdown("**Example CSV format:**")
sample_csv = """Ingredient,Quantity,Type
Chicken Breast (g),1500,wholesale
Olive Oil (ml),100,wholesale
Garlic Cloves,10,retail
Lemon (pcs),3,retail
Salt (g),20,wholesale
Black Pepper (g),5,wholesale
Roasted Vegetables Mix (g),1200,wholesale
Bread Rolls (pcs),10,retail
Butter (g),200,wholesale
Caesar Dressing (ml),300,wholesale
Parmesan Cheese (g),100,wholesale
Mixed Greens (g),500,wholesale
Tomatoes (pcs),5,retail
Cucumber (pcs),3,retail
Fruit Salad Mix (g),1500,wholesale
Cookies (pcs),20,retail
"""
st.code(sample_csv)

st.markdown(generate_csv_download_link(sample_csv, "sample_menu.csv"), unsafe_allow_html=True)
