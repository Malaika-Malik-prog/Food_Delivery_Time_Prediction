import streamlit as st
import pandas as pd
from data.database import create_table, register_user, login_user
from data.model import train_model, predict_delivery
model = train_model()

st.set_page_config(
    page_title="Food Delivery Time Prediction",
    page_icon="🍔",
    layout="wide"
)

create_table()

# Login and Signup
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🍔 Food Delivery Time Prediction")
    st.write("Welcome to our Food Delivery Prediction System!")

    choice = st.sidebar.selectbox("Menu", ["Login", "Signup"])

    if choice == "Signup":
        st.subheader("Create New Account")

        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Signup"):
            if username and email and password:
                if register_user(username, email, password):
                    st.success("Account created successfully!")
                else:
                    st.error("Username or Email already exists.")
            else:
                st.warning("Please fill all fields.")

    else:
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

# Main Dashboard
else:

    st.title("🍔 Food Delivery Dashboard")

    st.sidebar.success(
        f"Welcome {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    menu = st.sidebar.selectbox(
        "Dashboard Menu",
        ["Home", "Dataset", "Prediction"]
    )

    if menu == "Home":

        st.header("Dashboard Overview")
        st.write("Food Delivery Time Prediction System")

        col1, col2 = st.columns(2)

        col1.metric("Project", "Food Delivery")
        col2.metric("Status", "Active")

        st.info("Use the sidebar to explore the dashboard.")

    elif menu == "Dataset":

        st.header("Dataset Preview")

        try:
            df = pd.read_csv(
                "data/Food_Delivery_Times.csv")
            st.write(df.columns.tolist())

            st.success("Dataset loaded successfully!")

            st.write("Dataset Shape:", df.shape)

            st.dataframe(df.head(20))

            st.subheader("Dataset Statistics")
            st.write(df.describe())

            numeric_df = df.select_dtypes(
                include="number"
            )

            if not numeric_df.empty:
                st.subheader("Data Visualization")
                st.bar_chart(numeric_df.head(10))

        except FileNotFoundError:
            st.error("Dataset file not found!")

    elif menu == "Prediction":

        st.header("Food Delivery Time Prediction")

        distance = st.number_input(
            "Distance (KM)", min_value=0.1, value=5.0
        )

        preparation = st.number_input(
            "Preparation Time (Minutes)", min_value=1, value=15
        )

        experience = st.number_input(
            "Courier Experience (Years)", min_value=0.0, value=2.0
        )

        weather = st.selectbox(
            "Weather", ["Clear", "Rainy", "Foggy", "Windy", "Snowy"]
        )

        traffic = st.selectbox(
            "Traffic Level", ["Low", "Medium", "High"]
        )

        time_of_day = st.selectbox(
            "Time of Day", ["Morning", "Afternoon", "Evening", "Night"]
        )

        vehicle_type = st.selectbox(
            "Vehicle Type", ["Bike", "Scooter", "Car", "Bicycle"]
        )

        if st.button("Predict Delivery Time"):

            estimated_time = predict_delivery(
                model,
                distance,
                weather,
                traffic,
                time_of_day,
                vehicle_type,
                preparation,
                experience
            )

            st.success(
                f"Predicted Delivery Time: {estimated_time:.1f} minutes"
            )