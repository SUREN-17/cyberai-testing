from pydantic import BaseModel
from flask import Flask, render_template, request
import openpyxl
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import Optional

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()

class UserInput(BaseModel):
    msg: str

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    return lemmatized_tokens

def get_response(user_input):
    user_input = user_input.lower()
    wb = openpyxl.load_workbook('chat_bot.xlsx')
    sheet = wb.active
    
    response = None
    for row in sheet.iter_rows(values_only=True):
        if row[0] is not None and isinstance(row[0], str) and row[0].lower() == user_input:
            response = row[1] if row[1] is not None else None
            break
    
    wb.close()
    return response if response else "Sorry, I don't have an answer for that."

def recognize_intent(user_input):
    doc = nlp(user_input)
    tokens = preprocess_text(user_input)
    if any(token in ['greeting', 'hi', 'hello'] for token in tokens):
        return "Hello! How can I assist you?"
    return get_response(user_input)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get')
def get_bot_response():
    user_input = UserInput(msg=request.args.get('msg'))
    response = recognize_intent(user_input.msg)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
