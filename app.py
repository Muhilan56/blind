from flask import Flask, render_template, request
import speech_recognition as sr

app = Flask(__name__)

# Dummy user database for demonstration
users = {"user1": "password123"}

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        with microphone as source:
            print("Say something...")
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
            return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None

# Route for the main page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pay')
def pay():
    return render_template('payment.html')

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if users.get(username) == password:
        return render_template('payment.html', user=username)
    else:
        return "Invalid credentials, please try again!"

# Route for handling voice input for payment
@app.route('/payment', methods=['POST'])
def process_payment():
    # Start by capturing the voice input for payment command
    payment_command = recognize_speech()
    
    if payment_command == 'pay':
        # Simulating successful payment
        return "Payment processed successfully!"
    else:
        # If the command is not recognized or not "pay"
        return "No valid payment command detected. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
