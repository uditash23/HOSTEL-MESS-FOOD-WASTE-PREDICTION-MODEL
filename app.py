import joblib
import pandas as pd
import streamlit as st


@st.cache_resource
def load_model():
    model_data = joblib.load("hostel_mess_model.pkl")
    return model_data["model"], model_data["preprocessor"], model_data["features"]


model, preprocessor, features = load_model()

st.set_page_config(page_title="Hostel Mess Prediction", page_icon="🍽️", layout="centered")
st.title("Hostel Mess Prediction")
st.caption("Predict mess consumption using the trained machine learning model.")

with st.form("prediction_form"):
    students = st.number_input("Students", min_value=1, value=100, step=1)
    attendance = st.number_input("Attendance", min_value=0, value=75, step=1)
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner"])
    menu = st.selectbox("Menu", ["Veg", "Non-Veg", "Mixed"])
    weather = st.selectbox("Weather", ["Sunny", "Rainy", "Cloudy"])
    special_event = st.selectbox("Special Event", ["No", "Yes"])
    holiday = st.selectbox("Holiday", ["No", "Yes"])
    previous_consumption = st.number_input("Previous Consumption (kg)", min_value=0.0, value=10.0, step=0.5)

    submit = st.form_submit_button("Predict")

if submit:
    if attendance > students:
        st.warning("Attendance cannot exceed the total number of students.")
        st.stop()

    input_data = pd.DataFrame([{
        "Students": float(students),
        "Attendance": float(attendance),
        "Attendance_Rate": attendance / students,
        "Meal_Type": meal_type,
        "Menu": menu,
        "Weather": weather,
        "Special_Event": special_event,
        "Holiday": holiday,
        "Previous_Consumption_kg": float(previous_consumption),
        "Weekend": 0
    }])

    input_data = input_data[features]
    processed_data = preprocessor.transform(input_data)
    prediction = model.predict(processed_data)[0]
    recommended_quantity = prediction * 1.05

    st.success("Prediction complete")
    col1, col2 = st.columns(2)
    col1.metric("Predicted Consumption", f"{float(prediction):.2f} kg")
    col2.metric("Recommended Quantity", f"{float(recommended_quantity):.2f} kg")