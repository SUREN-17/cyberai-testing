import spacy
from flask import Flask, render_template, request
import openpyxl
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()

# Function to preprocess text using NLTK
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())  # Convert to lowercase and tokenize
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatize tokens
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    
    return lemmatized_tokens

# Function to get response from Excel based on user input
def get_response(user_input):
    user_input = user_input.lower()  # Convert user input to lowercase for case-insensitive comparison
    
    # Logic to retrieve response from Excel based on the user input
    wb = openpyxl.load_workbook('chat_bot.xlsx')
    sheet = wb.active
    
    response = None
    for row in sheet.iter_rows(values_only=True):
        # Add a check to handle empty rows and empty responses in the Excel file
        if row[0] is not None and isinstance(row[0], str) and row[0].lower() == user_input:
            response = row[1] if row[1] is not None else None  # Check for empty response
            break
    
    wb.close()
    return response if response else "Sorry, I don't have an answer for that."

# Function for intent recognition using spaCy and NLTK
def recognize_intent(user_input):
    doc = nlp(user_input)
    
    # Example logic - check for specific keywords or intents in the input using NLTK-processed tokens
    tokens = preprocess_text(user_input)
    if any(token in ['greeting', 'hi', 'hello'] for token in tokens):
        return "Hello! How can I assist you?"
    # Add more intent recognition logic based on your requirements
    
    # Default response if no specific intent is recognized
    return get_response(user_input)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    response = recognize_intent(userText)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
