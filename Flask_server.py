from flask import Flask, request, jsonify, render_template
import aiml
app = Flask(__name__)

kernal = aiml.Kernel()
kernal.learn("code2.aiml")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['input']
    if user_input:
        bot_response = kernal.respond(user_input)
        command = kernal.getPredicate("command")
        print("command:", command)
        if bot_response:
            print("command:", command)
            return jsonify(response=bot_response)
    return jsonify(response='Oops! Something went wrong.')

if __name__ == '__main__':
 app.run(host='0.0.0.0', port='5000')