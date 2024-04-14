from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data['question']
    answer = "I'm not even listening!!"  # Placeholder answer
    return jsonify(answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
