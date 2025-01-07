# Nutrition Deficiency Prediction

This project is a Streamlit-based web application that integrates Google Fit and Gemini AI to predict potential nutrition deficiencies and provide dietary suggestions based on user health and lifestyle inputs.

## Features
- **Google Fit Integration**: Fetch heart rate data from Google Fit.
- **User Input Form**: Collect user data, including weight, diet, alcohol consumption, smoking habits, and more.
- **Gemini AI Integration**: Use the Gemini API to analyze user data and generate predictions and dietary recommendations.
- **Interactive Visualizations**: Display heart rate data using line charts.

## Prerequisites
1. Python 3.8+
2. Streamlit
3. Google Fit API credentials
4. Gemini API access

## Installation

### Clone the Repository
```bash
$ git clone https://github.com/saishivamani1/nutrition-deficiency-prediction.git
$ cd nutrition-deficiency-prediction
```

### Set Up Virtual Environment
```bash
$ python -m venv env
$ source env/bin/activate # On Windows: env\Scripts\activate
```

### Install Dependencies
```bash
$ pip install -r requirements.txt
```

### Configure API Keys
1. **Google Fit API**: Download the `client_secrets.json` file from the Google Developer Console and place it in the project directory.
2. **Gemini API**: Set the `GENAI_API_KEY` variable in the code with your Gemini API key.

## Usage

### Run the Application
```bash
$ streamlit run app.py
```

### Authenticate with Google Fit
1. Open the local URL provided by Streamlit.
2. Click the authorization link to authenticate with Google Fit.
3. Paste the authorization code into the input box.

### Provide User Inputs
1. Fill out the form with your health and lifestyle details.
2. Submit the form to get predictions and suggestions.

## Project Structure
```
|-- app.py                 # Main application code
|-- client_secrets.json    # Google Fit API credentials (not included in the repository)
|-- requirements.txt       # Python dependencies
|-- README.md              # Project documentation
```

## Dependencies
- **Streamlit**: Web application framework
- **Google API Client**: To interact with Google Fit API
- **Pandas**: Data manipulation and analysis
- **Google Generative AI (Gemini)**: For AI-based predictions and recommendations

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue.

## Acknowledgments
- Google Fit API for health data
- Gemini AI for predictions and suggestions

## Contact
For any questions or suggestions, feel free to contact saishivamani@outlook.com .

