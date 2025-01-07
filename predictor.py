import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pandas as pd
import time
import google.generativeai as genai

# Configure Gemini API
GENAI_API_KEY = "api-key"
genai.configure(api_key=GENAI_API_KEY)

# Helper functions
def get_google_fit_data(service, data_source_id, start_time, end_time):
    dataset_id = f"{start_time}000000-{end_time}000000"
    try:
        dataset = service.users().dataSources().datasets().get(
            userId="me",
            dataSourceId=data_source_id,
            datasetId=dataset_id
        ).execute()
        return dataset
    except Exception as e:
        st.error(f"Error fetching Google Fit data: {e}")
        return {}

def parse_data(response, metric_name):
    data = []
    for point in response.get("point", []):
        start_time = int(point["startTimeNanos"]) / 1e9
        value = point["value"][0]
        data_value = value.get("fpVal") or value.get("intVal")
        data.append({
            "timestamp": pd.to_datetime(start_time, unit='s'),
            metric_name: data_value
        })
    return pd.DataFrame(data)

# OAuth setup
SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read',
          'https://www.googleapis.com/auth/fitness.heart_rate.read']
CLIENT_SECRETS_FILE = "client_secrets.json"

def authenticate_user():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:8501"
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    st.markdown(f"[Click here to authorize Google Fit access]({auth_url})")
    return flow

def fetch_heart_rate_data(service):
    data_source_id = "derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm"
    now = int(time.time() * 1000)
    seven_days_ago = now - (7 * 24 * 60 * 60 * 1000)
    response = get_google_fit_data(service, data_source_id, seven_days_ago, now)
    return parse_data(response, "Heart Rate (BPM)")

# Streamlit app
st.title("Nutrition Deficiency Prediction")

# Google Fit Authentication
if "credentials" not in st.session_state:
    flow = authenticate_user()
    code = st.text_input("Enter the authorization code here:")
    if code:
        try:
            flow.fetch_token(code=code)
            st.session_state["credentials"] = flow.credentials
            st.success("Authentication successful!")
        except Exception as e:
            st.error(f"Error during authentication: {e}")

if "credentials" in st.session_state:
    credentials = st.session_state["credentials"]
    service = build('fitness', 'v1', credentials=credentials)

    # Fetch and display Google Fit data
    try:
        st.subheader("Heart Rate Data")
        heart_rate_data = fetch_heart_rate_data(service)
        if not heart_rate_data.empty:
            st.line_chart(heart_rate_data.set_index("timestamp"))
        else:
            st.write("No heart rate data available.")
    except Exception as e:
        st.error(f"Error fetching heart rate data: {e}")

    # Collect user inputs
    st.subheader("Health and Lifestyle Inputs")
    with st.form("user_inputs"):
        gender = st.radio("Gender", ["Male", "Female"])
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, step=1)
        diet = st.radio("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        alcohol = st.slider("Alcohol Consumption (drinks per week)", 0, 20, 0)
        smoking = st.radio("Smoking Habit", ["Yes", "No"])
        drugs = st.radio("Drug Usage", ["Yes", "No"])
        sleep_time = st.slider("Average Sleep Time (hours per day)", 4, 12, 8)
        if gender == "Female":
            periods = st.radio("Are your periods regular?", ["Yes", "No"])

        submit = st.form_submit_button("Submit")

    if submit:
        # Prepare data for Gemini API
        user_data = {
            "gender": gender,
            "weight": weight,
            "diet": diet,
            "alcohol": alcohol,
            "smoking": smoking,
            "drugs": drugs,
            "sleep_time": sleep_time,
            "heart_rate_data": heart_rate_data.to_dict(orient="records"),
        }
        if gender == "Female":
            user_data["periods"] = periods

        # Call Gemini AI for predictions
        st.subheader("Predictions and Suggestions")
        try:
            model = genai.GenerativeModel('gemini-pro')
            gemini_prompt = f"Analyze the following data to predict potential nutrition deficiencies and provide dietary suggestions. Be specific in recommendations:\n\n{user_data}"
            
            response = model.generate_content(gemini_prompt)
            st.success("Prediction and Suggestions")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error querying Gemini AI: {e}")
