# frontend.py
from dash import Dash, html, dcc, Input, Output, State
import requests

app = Dash(__name__, title='Simple Mailer')

app.layout = html.Div([
    html.Div([
        html.H2("Envoyer un email", style={
            'textAlign': 'center',
            'color': '#ffffff',
            'fontFamily': 'Arial, sans-serif'
        }),
        dcc.Input(id='server', type='text', placeholder='SMTP server', value='smtp.example.com', style={
            'margin': '10px 0',  # Adjusted margin for consistency
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff'
        }),
        dcc.Input(id='port', type='number', placeholder='Port', value=587, style={
            'margin': '10px 0',  # Adjusted margin for consistency
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff'
        }),
        dcc.Input(id='username', type='text', placeholder='Username', style={
            'margin': '10px 0',  # Adjusted margin for consistency
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff'
        }),
        dcc.Input(id='password', type='password', placeholder='Password', style={
            'margin': '10px 0',  # Adjusted margin for consistency
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff'
        }),
        dcc.Input(id='sender', type='text', placeholder='From address', style={
            'margin': '10px 0',  # Adjusted margin for consistency
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff'
        }),
        dcc.Textarea(id='recipients', placeholder='Destinataires (virgule séparés)', style={
            'margin': '10px 0',  # Adjusted margin for consistency
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'height': '80px',
            'backgroundColor': '#333',
            'color': '#fff'
        }),
        dcc.Input(id='subject', type='text', placeholder='Sujet', style={
            'margin': '10px 0',  # Adjusted margin for consistency
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff'
        }),
        dcc.Textarea(id='body', placeholder='Corps du message (HTML ok)', style={
            'margin': '10px 0',  # Adjusted margin for consistency
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'height': '120px',
            'backgroundColor': '#333',
            'color': '#fff'
        }),
        html.Button('Envoyer', id='send-btn', style={
            'margin': '10px 0',  # Adjusted margin for consistency
            'backgroundColor': '#007BFF',
            'color': 'white',
            'border': 'none',
            'padding': '10px 20px',
            'cursor': 'pointer',
            'borderRadius': '5px',
            'fontSize': '16px',
            'width': '100%'
        },
        n_clicks=0),
        html.Div(id='status', style={
            'marginTop': '20px',
            'textAlign': 'center',
            'fontWeight': 'bold',
            'fontFamily': 'Arial, sans-serif',
            'color': '#ffffff'
        })
    ], style={
        'width': '400px',
        'margin': '50px auto',
        'padding': '20px',
        'border': '1px solid #444',
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
        'backgroundColor': '#222',
        'fontFamily': 'Arial, sans-serif'
    })
], style={
    'backgroundColor': '#121212',
    'minHeight': '100vh',
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'center'
})

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