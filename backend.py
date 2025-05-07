# backend.py
from flask import Flask, request, jsonify
from email_service import send_mail

app = Flask(__name__)

@app.route('/api/send', methods=['POST'])
def api_send():
    data = request.get_json()
    try:
        send_mail(
            server    = data['server'],
            port      = data['port'],
            username  = data['username'],
            password  = data['password'],
            sender    = data['sender'],
            recipients= data['recipients'],
            subject   = data['subject'],
            body      = data['body'],
        )
        return jsonify(status='ok'), 200
    except Exception as e:
        return jsonify(status='error', message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
