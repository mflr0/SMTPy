# frontend.py
from dash import Dash, html, dcc, Input, Output, State
import requests

app = Dash(__name__, title='Simple Mailer')

app.layout = html.Div([
    html.H2("Envoyer un email"),
    dcc.Input(id='server',     type='text', placeholder='SMTP server', value='smtp.example.com'),
    dcc.Input(id='port',       type='number', placeholder='Port', value=587),
    dcc.Input(id='username',   type='text', placeholder='Username'),
    dcc.Input(id='password',   type='password', placeholder='Password'),
    dcc.Input(id='sender',     type='text', placeholder='From address'),
    dcc.Textarea(id='recipients', placeholder='Destinataires (virgule séparés)'),
    dcc.Input(id='subject',    type='text', placeholder='Sujet'),
    dcc.Textarea(id='body',     placeholder='Corps du message (HTML ok)'),
    html.Button('Envoyer', id='send-btn'),
    html.Div(id='status')
], style={'width':'400px', 'margin':'auto'})

@app.callback(
    Output('status', 'children'),
    Input('send-btn', 'n_clicks'),
    State('server', 'value'),
    State('port', 'value'),
    State('username', 'value'),
    State('password', 'value'),
    State('sender', 'value'),
    State('recipients', 'value'),
    State('subject', 'value'),
    State('body', 'value'),
)
def on_send(n, server, port, username, password, sender, recips, subject, body):
    if not n:
        return ""
    data = {
        "server": server,
        "port": port,
        "username": username,
        "password": password,
        "sender": sender,
        "recipients": [r.strip() for r in recips.split(',') if r.strip()],
        "subject": subject,
        "body": body
    }
    try:
        r = requests.post("http://localhost:5000/api/send", json=data)
        if r.ok:
            return "✅ Email envoyé !"
        else:
            return f"❌ Erreur : {r.json().get('message')}"
    except Exception as e:
        return f"❌ Impossible de contacter le serveur : {e}"

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
