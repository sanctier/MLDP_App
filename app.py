import streamlit as st
import pandas as pd
import joblib
import base64
import os
# Load model
model = joblib.load("rfmodel_compressed.pkl")

# Convert GIF to base64 for background
def get_base64_gif(gif_path):
    with open(gif_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

gif_base64 = get_base64_gif("diamond_falling.gif")


st.markdown(f"""
    <style>
    .stApp {{
        background: url("data:image/gif;base64,{gif_base64}") no-repeat center center fixed;
        background-size: cover;
    }}

    .block-container {{
        background-color: rgba(255, 255, 255, 0.85);
        color: black;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }}

    .stButton button {{
        background: linear-gradient(to right, #77FFA4, #C3B6F6);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: bold;
        color: #000;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        transition: 0.3s ease-in-out;
    }}

    .stButton button:hover {{
        transform: scale(1.05);
        background: linear-gradient(to right, #C3B6F6, #77FFA4);
        color: #000;
    }}

    h1, h2, h3, h4, h5, h6, label, .stMarkdown, .stTextInput label, .stNumberInput label {{
        color: black !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Title of the app
st.title("💎 Diamond Price Predictor")

# Form User Interface
st.markdown('<div class="centered">', unsafe_allow_html=True)
st.subheader("Enter Diamond Features")

col1 = st.columns(1)[0]
carat = col1.number_input("Carat", min_value=0.0, max_value=50.0, step=0.01, value=0.7)

colx, coly, colz = st.columns(3)
with colx:
    x = st.number_input("Length (x)", min_value=0.0, max_value=1000.0, step=0.01, value=4.0)
with coly:
    y = st.number_input("Width (y)", min_value=0.0, max_value=1000.0, step=0.01, value=4.0)
with colz:
    z = st.number_input("Depth (z)", min_value=0.0, max_value=1000.0, step=0.01, value=2.5)

volume = x * y * z

cut = st.selectbox("Cut", ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'])
color = st.selectbox("Color", ['D', 'E', 'F', 'G', 'H', 'I', 'J'])
clarity = st.selectbox("Clarity", ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'])

def create_input_df():
    input_dict = {
        'carat': carat,
        'volume': volume
    }
    for option in ['Good', 'Very Good', 'Premium', 'Ideal']:
        input_dict[f'cut_{option}'] = 1 if cut == option else 0
    for option in ['E', 'F', 'G', 'H', 'I', 'J']:
        input_dict[f'color_{option}'] = 1 if color == option else 0
    for option in ['SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']:
        input_dict[f'clarity_{option}'] = 1 if clarity == option else 0
    return pd.DataFrame([input_dict])

# Prediction
if st.button("💎 Predict Price"):
    input_df = create_input_df()

    if carat > 5.0 or volume > 500.0:
        st.markdown(f"""
        <div style="
            background-color: #ff7777;
            padding: 1rem 2rem;
            border-radius: 12px;
            color: #000000;
            font-size: 1.2rem;
            font-weight: bold;
            text-align: center;
            margin-top: 1.5rem;">
            This is a rare diamond, our model cannot predict the price accurately.
        </div>
        """, unsafe_allow_html=True)
    else:
        usd_to_sgd = 1.28  
        prediction = model.predict(input_df)
        price_usd = prediction[0]
        price_sgd = price_usd * usd_to_sgd

        st.markdown(f"""
        <div style="
            background-color: rgba(255, 255, 255, 0.8);
            border: 2px solid #000000;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            color: #000000;
            font-size: 1.4rem;
            font-weight: bold;
            text-align: center;
            margin-top: 1.5rem;">
            Estimated Price<br><br>
            USD: ${price_usd:,.2f}<br>
            SGD: ${price_sgd:,.2f}
        </div>
        """, unsafe_allow_html=True)



st.markdown('</div>', unsafe_allow_html=True)

# Fun facts section
st.markdown("""
    <hr style="border-top: 2px solid #aaa; margin-top: 3rem;">
    <div style="text-align: center; padding: 1rem; color: black;">
        <h4>💎 Fun Facts About Diamonds</h4>
        <ul style="list-style-type: none; padding-left: 0;">
            <li>The largest diamond ever found was the Cullinan diamond — it weighed 3,106 carats!</li>
            <li>Diamonds are over 3 billion years old and form deep beneath the Earth's surface.</li>
            <li>A diamond can actually burn! It turns into carbon dioxide if exposed to extreme heat.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
