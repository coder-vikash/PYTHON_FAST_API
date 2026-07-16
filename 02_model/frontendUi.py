import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://localhost:8000/predict"

# Page Configuration
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="💰",
    layout="centered"
)

# Title
st.title("💰 Insurance Premium Category Predictor")
st.write("Fill in your details to predict your insurance premium category.")

st.divider()

# -------------------------
# User Inputs
# -------------------------

age = st.number_input(
    "Age",
    min_value=1,
    max_value=119,
    value=25
)

weight = st.number_input(
    "Weight (Kg)",
    min_value=1.0,
    value=65.0
)

height = st.number_input(
    "Height (m)",
    min_value=0.5,
    max_value=2.5,
    value=1.70
)

income_lpa = st.number_input(
    "Annual Income (LPA)",
    min_value=0.1,
    value=10.0
)

smoker = st.selectbox(
    "Are you a smoker?",
    [True, False]
)

city = st.text_input(
    "City",
    value="Mumbai"
)

occupation = st.selectbox(
    "Occupation",
    [
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job"
    ]
)

st.divider()


# -------------------------
# Predict Button
# -------------------------

if st.button("Predict Premium Category"):

    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:

        response = requests.post(
            API_URL,
            json=payload
        )

        if response.status_code == 200:

            result = response.json()

            st.success("Prediction Successful!")

            st.subheader("Predicted Category")

            st.info(
                result["predicted_category"]
            )

        else:

            st.error(
                f"API Error : {response.status_code}"
            )

            st.write(response.json())


    except Exception as e:

        st.error("Could not connect to FastAPI Server.")
        st.write(e)