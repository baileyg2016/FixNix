from flask import Flask, request, jsonify

app = Flask(__name__)
app.debug = True

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print('Received a request', data)
    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']})
    else:
        return jsonify({'message': 'No challenge parameter found'}), 400

if __name__ == '__main__':
    app.run(port=8080)