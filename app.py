from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para flash messages e sessões

# Função para carregar os dados do arquivo 'data.txt'
def carregar_dados():
    moderadores = {}
    with open('data.txt', 'r') as f:
        for linha in f:
            email, senha, torneios_acesso = linha.strip().split(',')
            torneios_ids = list(map(int, torneios_acesso.split()))  # IDs dos torneios
            moderadores[email] = {'senha': senha, 'torneios': torneios_ids}
    return moderadores

# Carrega os dados dos moderadores ao iniciar o servidor
moderadores = carregar_dados()

# Dados de torneios para exibição (exemplo fictício)
torneios = [
    {
        'id': 1,
        'name': '[INTER] Falcons Button Mash #13 - Darkstalkers',
        'description': 'Organizado por AcadArena Brasil • Brasil • 1v1 • 16 slots',
        'image': '/static/images/falcons_button_mash.png',
        'date': 'Amanhã, 20:00',
        'status': 'upcoming',
        'teams': ['Equipe A', 'Equipe B']
    },
    {
        'id': 2,
        'name': '[INTER] Falcons Challenge - SEMEC - Street Fighter 6',
        'description': 'Organizado por AcadArena Brasil • BR • 1v1 • 8 slots',
        'image': '/static/images/falcons_street_fighter.png',
        'date': 'Tuesday, 09:30',
        'status': 'upcoming',
        'teams': ['Equipe C', 'Equipe D']
    },
    {
        'id': 3,
        'name': '[INTER] Falcons Challenge - SEMEC - League of Legends (1x1)',
        'description': 'Organizado por AcadArena Brasil • BR • 1v1 • 16 slots',
        'image': 'https://image1.challengermode.com/13f1e241-3154-4d16-7751-08dcdb4c5329_1200_300',
        'date': 'Tuesday, 09:30',
        'status': 'upcoming',
        'teams': ['Equipe E', 'Equipe F']
    },
    {
        'id': 4,
        'name': '[Inters] SEMCOMP Valorant',
        'description': 'Organizado por AcadArena Brasil • Brasil • 5v5 • 1º Lugar 1.600VP / 2º Lugar 1.400VP',
        'image': 'https://image1.challengermode.com/fa05727f-97eb-470d-864d-08dcdb4c5329_1200_300',
        'date': 'Thursday, 19:30',
        'status': 'upcoming',
        'teams': ['Equipe G', 'Equipe H']
    },
    {
        'id': 5,
        'name': '[Inters] InterUNIFEI 2024.2 - League of Legends',
        'description': 'Organizado por AcadArena Brasil • BR • 5v5 • 16 slots',
        'image': 'https://image1.challengermode.com/d5ef0fd4-1bb6-45d8-0028-08dc4dd732f6_1200_300',
        'date': 'Sat, October 26, 15:00',
        'status': 'upcoming',
        'teams': ['Equipe I', 'Equipe J']
    },
    {
        'id': 6,
        'name': '[Inter] Arena FEI Valorant 2024',
        'description': 'Organizado por AcadArena Brasil • 5v5 • 16 slots',
        'image': 'https://image1.challengermode.com/f2abc578-a3d6-4926-7bf1-08dcb2cf0beb_1200_300',
        'date': 'Sat, October 26, 18:00',
        'status': 'upcoming',
        'teams': ['Equipe K', 'Equipe L']
    },
    {
        'id': 7,
        'name': 'ACES Inclusivo - Valorant 2024.2',
        'description': 'Organizado por AcadArena Brasil • Brasil • 5v5 • 1º Lugar: 1 Skin Deluxe por jogadora titular',
        'image': 'https://image1.challengermode.com/dce013fc-be0f-426c-dbdc-08dcce7daa18_2400_600',  
        'date': 'Sun, October 27, 13:00',
        'status': 'upcoming',
        'teams': ['Equipe M', 'Equipe N']
    },
    {
        'id': 8,
        'name': '[Inters] InterUNIFEI 2024.2 - VALORANT',
        'description': 'Organizado por AcadArena Brasil • Brasil • 5v5 • 16 slots',
        'image': 'https://image1.challengermode.com/5671ab26-fd85-4297-2b70-08dc4dd2d708_1200_300',  
        'date': 'Sun, October 27, 15:00',
        'status': 'upcoming',
        'teams': ['Equipe O', 'Equipe P']
    },
    {
        'id': 9,
        'name': 'ACES Open - League of Legends',
        'description': 'Organizado por AcadArena Brasil • BR • 5v5 • 1º Lugar: 1 Skin Épica por jogador titular',
        'image': 'https://image1.challengermode.com/b6b29662-1aaf-43fe-dbec-08dcce7daa18_1200_300',  # Adicione a imagem correta
        'date': 'Sat, November 02, 13:00',
        'status': 'upcoming',
        'teams': ['Equipe Q', 'Equipe R']
    },
    {
        'id': 10,
        'name': 'ACES Inclusivo - Wild Rift 2024.2',
        'description': 'Organizado por AcadArena Brasil • 5v5 • 1º Lugar: 1 Skin Épica por jogador titular',
        'image': 'https://image1.challengermode.com/55cc9c81-0b99-4c93-dbf4-08dcce7daa18_1200_300',  # Adicione a imagem correta
        'date': 'Sat, November 09, 13:00',
        'status': 'upcoming',
        'teams': ['Equipe S', 'Equipe T']
    },
    {
        'id': 11,
        'name': 'ACES Open - Valorant',
        'description': 'Organizado por AcadArena Brasil • 5v5 • 1º Lugar: 1 Skin Deluxe por jogadora titular',
        'image': '/static/images/aces_inclusivo_valorant.png',  # Adicione a imagem correta
        'date': 'Sat, November 09, 13:00',
        'status': 'upcoming',
        'teams': ['Equipe U', 'Equipe V']
    },
     {
        'id': 12,
        'name': '[Inters] Campeonato de X1 PUC-Rio',
        'description': 'Organizado por AcadArena Brasil • BR • 1v1 • 16 slots',
        'image': 'https://image1.challengermode.com/d5ef0fd4-1bb6-45d8-0028-08dc4dd732f6_2400_600',
        'date': 'Há 8 dias',
        'status': 'in_progress',
        'teams': ['Equipe W', 'Equipe X']
    },
    {
        'id': 13,
        'name': 'Copa Aliança - League of Legends Fase de Grupos + Playoffs 2024.2',
        'description': 'Organizado por AcadArena Brasil • BR • 5v5 • 16 slots',
        'image': 'https://image1.challengermode.com/c77c501b-41a7-43e8-2644-08dcdb50ab9c_1200_300',
        'date': 'Há 14 dias',
        'status': 'in_progress',
        'teams': ['Equipe Y', 'Equipe Z']
    },
    {
        'id': 14,
        'name': 'Copa Aliança - Valorant Fase de Grupos + Playoffs 2024.2',
        'description': 'Organizado por AcadArena Brasil • Brasil • 5v5 • 16 slots',
        'image': 'https://image1.challengermode.com/df367481-06e1-41f8-264d-08dcdb50ab9c_1200_300',
        'date': 'Há 14 dias',
        'status': 'in_progress',
        'teams': ['Equipe Alpha', 'Equipe Beta']
    },
    {
        'id': 15,
        'name': 'Copa Aliança - TFT 2024.2',
        'description': 'Organizado por AcadArena Brasil • BR • 1v1 • 64 vagas para Fase de Grupos • 64 slots',
        'image': 'https://image1.challengermode.com/1e8fa8c4-204f-43e4-5255-08dcc4877eb6_1200_300',
        'date': 'Há 21 dias',
        'status': 'in_progress',
        'teams': ['Equipe Gamma', 'Equipe Delta']
    },
    {
        'id': 16,
        'name': 'Copa Aliança - Wild Rift 2024.2',
        'description': 'Organizado por AcadArena Brasil • BR • 5v5 • 8 slots',
        'image': 'https://image1.challengermode.com/023c5b30-5518-43c4-523f-08dcc4877eb6_1200_300',
        'date': 'Há 28 dias',
        'status': 'in_progress',
        'teams': ['Equipe Omega', 'Equipe Sigma']
    },

     {
        'id': 17,
        'name': 'Copa Aliança - Wild Rift 2024.2',
        'description': 'Organizado por AcadArena Brasil • Brasil • 5v5 • 16 vagas para a Fase de Grupos • 8 slots',
        'image': 'https://image1.challengermode.com/023c5b30-5518-43c4-523f-08dcc4877eb6_1200_300',
        'date': 'Há 28 dias',
        'status': 'in_progress',
        'teams': ['Equipe Alpha', 'Equipe Beta']
    },
    {
        'id': 18,
        'name': '[Inters] Copa Marte - League of Legends',
        'description': 'Organizado por AcadArena Brasil • BR • 5v5 • 7 slots',
        'image': 'https://image1.challengermode.com/d5ef0fd4-1bb6-45d8-0028-08dc4dd732f6_1200_300',
        'date': 'Há cerca de 2 meses',
        'status': 'in_progress',
        'teams': ['Equipe Delta', 'Equipe Epsilon']
    },
    {
        'id': 19,
        'name': '[Inters] IntegraCUP Azure Bears 2024 - Valorant',
        'description': 'Organizado por AcadArena Brasil • Brasil • 5v5 • 6 slots',
        'image': 'https://image1.challengermode.com/e255a267-3b53-4f3e-f0c9-08dc630c46df_1200_300',
        'date': 'Há 4 meses',
        'status': 'in_progress',
        'teams': ['Equipe Sigma', 'Equipe Lambda']
    },
    {
        'id': 20,
        'name': '[Inters] IntegraCUP Azure Bears 2024 - League of Legends',
        'description': 'Organizado por AcadArena Brasil • BR • 5v5 • 7 slots',
        'image': 'https://image1.challengermode.com/e255a267-3b53-4f3e-f0c9-08dc630c46df_1200_300',
        'date': 'Há 4 meses',
        'status': 'in_progress',
        'teams': ['Equipe Gamma', 'Equipe Zeta']
    },
    {
        'id': 21,
        'name': '[Inters] IntegraCUP Azure Bears 2024 - Rocket League',
        'description': 'Organizado por AcadArena Brasil • Brasil • 2v2 • 6 slots',
        'image': 'https://image1.challengermode.com/dadeafaa-dd0a-43ac-c710-08dc630c46df_1200_300',
        'date': 'Há 4 meses',
        'status': 'in_progress',
        'teams': ['Equipe Theta', 'Equipe Iota']
    },
    {
        'id': 22,
        'name': '[Inters] IntegraCUP Azure Bears 2024 - CS2',
        'description': 'Organizado por AcadArena Brasil • Brasil • 5v5 • 5 slots',
        'image': 'https://image1.challengermode.com/bdc844e2-34c3-4c7b-c2dc-08dc630c46df_1200_300',
        'date': 'Há 4 meses',
        'status': 'in_progress',
        'teams': ['Equipe Kappa', 'Equipe Lambda']
    }

]

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Verifica as credenciais no dicionário 'moderadores'
        if email in moderadores and moderadores[email]['senha'] == password:
            session['user'] = email  # Cria uma sessão
            session['torneios_acesso'] = moderadores[email]['torneios']  # IDs dos torneios que o moderador pode acessar
            return redirect(url_for('home'))  # Redireciona para a página home
        else:
            flash('Login ou senha incorretos!')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/detalhes/<int:torneio_id>')
def detalhes(torneio_id):
    # Verifica se o moderador tem acesso ao torneio
    if torneio_id in session.get('torneios_acesso', []):
        torneio = next((t for t in torneios if t['id'] == torneio_id), None)
        if torneio:
            return render_template('detalhes.html', torneio=torneio)
        else:
            flash('Torneio não encontrado!', 'danger')  # Mensagem de erro para torneio não encontrado
            return redirect(url_for('torneios_ativos'))  # Redireciona para a página inicial (ou uma página apropriada)
    else:
        flash('Acesso não autorizado!', 'danger')  # Mensagem de erro para acesso não autorizado
        return redirect(url_for('torneios_ativos'))  # Redireciona para a página inicial (ou uma página apropriada)


# Página Home (Lista de torneios ativos)
@app.route('/home')
def home():
    if 'user' in session:
        torneios_permitidos = [t for t in torneios if t['id'] in session['torneios_acesso']]
        return render_template('home.html', torneios=torneios_permitidos)  # Exibe apenas os torneios que o moderador tem acesso
    else:
        return redirect(url_for('login'))

# Página Meus Torneios
@app.route('/meus_torneios')
def meus_torneios():
    if 'user' in session:
        # Filtra os torneios de acordo com os IDs que o moderador tem acesso
        meus_torneios_filtrados = [t for t in torneios if t['id'] in session['torneios_acesso']]
        return render_template('meus_torneios.html', torneios=meus_torneios_filtrados)
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

# Página Torneios Ativos
@app.route('/torneios_ativos')
def torneios_ativos():
    if 'user' in session:
        return render_template('torneios_ativos.html', torneios=torneios)  # Exibe todos os torneios
    else:
        return redirect(url_for('login'))
    
@app.route('/adicionar_meu_torneio/<int:torneio_id>', methods=['POST'])
def adicionar_meu_torneio(torneio_id):
    if 'user' in session:
        email = session['user']
        torneios_acesso = moderadores[email]['torneios']

        # Verifica se o torneio já não está na lista
        if torneio_id not in torneios_acesso:
            torneios_acesso.append(torneio_id)
            # Atualiza o arquivo data.txt
            atualizar_data_txt(email, torneios_acesso)
        flash(f'Torneio {torneio_id} adicionado com sucesso!', 'success')
        return redirect(url_for('torneios_ativos'))
    else:
        return redirect(url_for('login'))

# Rota para remover um torneio dos meus torneios
@app.route('/remover_meu_torneio/<int:torneio_id>', methods=['POST'])
def remover_meu_torneio(torneio_id):
    if 'user' in session:
        email = session['user']
        torneios_acesso = moderadores[email]['torneios']

        # Verifica se o torneio está na lista
        if torneio_id in torneios_acesso:
            torneios_acesso.remove(torneio_id)
            # Atualiza o arquivo data.txt
            atualizar_data_txt(email, torneios_acesso)
        flash(f'Torneio {torneio_id} removido com sucesso!', 'success')
        print(torneios_acesso)
        return redirect(url_for('meus_torneios'))
    else:
        return redirect(url_for('login'))

@app.route('/comunicar_equipe/<int:torneio_id>/<team_name>', methods=['GET', 'POST'])
def comunicar_equipe(torneio_id, team_name):
    if request.method == 'POST':
        # Pegando as tags do formulário e separando por vírgula
        tags = request.form.get('tags').split(',')
        # Removendo espaços em branco ao redor das tags
        tags = [tag.strip() for tag in tags]

        # Pegando o tipo de mensagem
        tipo_mensagem = request.form.get('prioridade')


        ## Processar as informações e enviar a mensagem para a equipe

        # Exemplo de uso das informações processadas
        flash(f'Mensagem enviada para a equipe {team_name} com sucesso! Tags: {tags}, Tipo: {tipo_mensagem}', 'success')

        # Redirecionar para a página de detalhes
        return redirect(url_for('detalhes', torneio_id=torneio_id))

    # Renderizar o formulário de comunicação
    return render_template('comunicar_equipe.html', team_name=team_name, torneio_id=torneio_id)


# função para enviar email para o capitão dois dias antes do torneio

# def envio_automatico_email():
#     from automatic_sender import automatic_sender

#     try:
#         automatic_sender()
#         # adc um check no html
#     except Exception as e:
#         print(f"Erro ao executar o envio de emails: {e}")


# Função para atualizar o arquivo data.txt
def atualizar_data_txt(email, torneios_atualizados):
    # Atualiza o dicionário dos moderadores com os novos IDs
    moderadores[email]['torneios'] = torneios_atualizados
    
    # Reescreve o arquivo data.txt com as informações atualizadas
    with open('data.txt', 'w') as f:
        for moderador, dados in moderadores.items():
            senha = dados['senha']
            torneios_ids = ' '.join(map(str, dados['torneios']))
            f.write(f"{moderador},{senha},{torneios_ids}\n")


# Rota de logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('torneios_acesso', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
