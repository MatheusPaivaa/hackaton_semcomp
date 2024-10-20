from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para flash messages e sessões

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'felipe_abud' and password == 'admin':
            session['user'] = email  # Cria uma sessão
            return redirect(url_for('home'))  # Redireciona para a página home
        else:
            flash('Login ou senha incorretos!')
            return redirect(url_for('login'))

    return render_template('login.html')

# Página Home
@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/torneios_ativos')
def torneios_ativos():
    if 'user' in session:
        # Exemplo de dados de torneios com status
        torneios = [
            {"name": "Torneio 1", "date": "20/10/2024", "description": "Torneio de FPS para iniciantes.", "image": "/static/images/torneio1.jpg", "status": "in_progress", "url": "#"},
            {"name": "Torneio 2", "date": "25/10/2024", "description": "Torneio de MOBA - Inscrição gratuita.", "image": "/static/images/torneio2.jpg", "status": "upcoming", "url": "#"},
            {"name": "Torneio 3", "date": "30/10/2024", "description": "Campeonato de RPG tático.", "image": "/static/images/torneio3.jpg", "status": "upcoming", "url": "#"}
        ]
        return render_template('torneios_ativos.html', torneios=torneios)
    else:
        return redirect(url_for('login'))

# Página Meus Torneios
@app.route('/meus_torneios')
def meus_torneios():
    if 'user' in session:
        return render_template('meus_torneios.html')
    else:
        return redirect(url_for('login'))

        

# Página Notificações
@app.route('/notificacoes')
def notificacoes():
    if 'user' in session:
        return render_template('notificacoes.html')
    else:
        return redirect(url_for('login'))

# Página Perfil
@app.route('/perfil')
def perfil():
    if 'user' in session:
        return render_template('perfil.html')
    else:
        return redirect(url_for('login'))

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
