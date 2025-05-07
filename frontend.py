# frontend.py
from dash import Dash, html, dcc, Input, Output, State
import requests

app = Dash(__name__, title='Simple Mailer')

app.layout = html.Div([
    html.Div([
        html.H2("🌟 Envoyer un email 🌟", style={
            'textAlign': 'center',
            'color': '#ffffff',
            'fontFamily': 'Arial, sans-serif',
            'margin': '0'  # Ensure no extra margin
        }),
        dcc.Input(id='server', type='text', placeholder='🌐 SMTP server', value='smtp.example.com', style={
            'margin': '10px auto',  # Centered and consistent margin
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff',
            'boxSizing': 'border-box'  # Prevent overflow
        }),
        dcc.Input(id='port', type='number', placeholder='🔌 Port', value=587, style={
            'margin': '10px auto',
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff',
            'boxSizing': 'border-box'
        }),
        dcc.Input(id='username', type='text', placeholder='👤 Username', style={
            'margin': '10px auto',
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff',
            'boxSizing': 'border-box'
        }),
        dcc.Input(id='password', type='password', placeholder='🔒 Password', style={
            'margin': '10px auto',
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff',
            'boxSizing': 'border-box'
        }),
        dcc.Input(id='sender', type='text', placeholder='📧 From address', style={
            'margin': '10px auto',
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff',
            'boxSizing': 'border-box'
        }),
        dcc.Textarea(id='recipients', placeholder='📜 Destinataires (virgule séparés)', style={
            'margin': '10px auto',
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'height': '80px',
            'backgroundColor': '#333',
            'color': '#fff',
            'boxSizing': 'border-box'
        }),
        dcc.Input(id='subject', type='text', placeholder='✉️ Sujet', style={
            'margin': '10px auto',
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'backgroundColor': '#333',
            'color': '#fff',
            'boxSizing': 'border-box'
        }),
        dcc.Textarea(id='body', placeholder='📝 Corps du message (HTML ok)', style={
            'margin': '10px auto',
            'padding': '10px',
            'border': '1px solid #555',
            'borderRadius': '5px',
            'width': '100%',
            'height': '120px',
            'backgroundColor': '#333',
            'color': '#fff',
            'boxSizing': 'border-box'
        }),
        html.Button('🚀 Envoyer', id='send-btn', style={
            'margin': '10px auto',
            'backgroundColor': '#007BFF',
            'color': 'white',
            'border': 'none',
            'padding': '10px 20px',
            'cursor': 'pointer',
            'borderRadius': '5px',
            'fontSize': '16px',
            'width': '100%',
            'boxSizing': 'border-box'
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
        'fontFamily': 'Arial, sans-serif',
        'boxSizing': 'border-box'  # Prevent overflow
    }),
    html.Footer([
        html.Div([
            html.A([
                html.Img(src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", 
                         style={'width': '20px', 'verticalAlign': 'middle', 'marginRight': '10px'})
            ], href="https://github.com/0xGuigui/SMTPy", target="_blank", style={'marginLeft': '10px'}),  # Shifted right
            html.A([
                html.Img(src="https://cdn-icons-png.flaticon.com/512/174/174857.png", 
                         style={'width': '20px', 'verticalAlign': 'middle'})
            ], href="https://www.linkedin.com/in/0xguigui", target="_blank", style={'marginLeft': '10px'})  # Shifted right
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'gap': '10px',
            'justifyContent': 'flex-start',
            'width': '33%'
        }),
        html.Div("Developed by 0xGuigui", style={
            'textAlign': 'center',
            'fontFamily': 'Arial, sans-serif',
            'color': '#ffffff',
            'width': '33%'
        }),
        html.Div(style={'width': '33%'})  # Empty div for spacing
    ], style={
        'position': 'relative',
        'width': '100%',
        'backgroundColor': '#222',
        'color': '#ffffff',
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'padding': '10px 20px',
        'boxShadow': '0 -2px 5px rgba(0, 0, 0, 0.2)',
        'marginTop': 'auto'  # Push footer to the bottom of the page
    })
], style={
    'backgroundColor': '#121212',
    'minHeight': '100vh',
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'center',
    'justifyContent': 'flex-start',  # Allow content to stack above the footer
    'backgroundImage': 'url("https://www.transparenttextures.com/patterns/stardust.png")',
    'backgroundSize': 'cover',
    'margin': '0',  # Remove any default margin
    'padding': '0',  # Remove any default padding
    'boxSizing': 'border-box'  # Prevent overflow
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