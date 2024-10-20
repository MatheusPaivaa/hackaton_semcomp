import pandas as pd
from datetime import datetime, timedelta
from email_sender import buscar_e_enviar_email

def verificar_e_enviar_emails(usuarios_csv, partidas_csv, remetente, senha):
    try:
        # Ler os arquivos CSV
        usuarios = pd.read_csv(usuarios_csv, encoding='utf-8')
        partidas = pd.read_csv(partidas_csv, encoding='utf-8')

        # Verifica cada partida para determinar se está próxima
        for _, partida in partidas.iterrows():
            data_partida = datetime.strptime(partida['data_partida'], '%Y-%m-%d')
            dias_para_partida = (data_partida - datetime.now()).days

            # Se faltarem menos de 2 dias, enviar email aos capitães dos times envolvidos
            if dias_para_partida < 2:
                time1 = partida['time1']
                time2 = partida['time2']

                # Encontrar os capitães dos times no CSV de usuários
                for time in [time1, time2]:
                    capitao = usuarios[
                        (usuarios['Time'] == time) & 
                        (usuarios['Cargo (Capitão ou jogador)'].str.lower() == 'capitão')
                    ]

                    if not capitao.empty:
                        email = capitao.iloc[0]['E-mail']
                        nome = capitao.iloc[0]['Nome Completo']
                        id_participante = capitao.iloc[0]['ID']

                        print(f"Enviando email para o capitão {nome} (Time: {time})")

                        # Enviar email usando a função buscar_e_enviar_email
                        buscar_e_enviar_email(
                            id_participante, usuarios_csv, partidas_csv, remetente, senha
                        )
                    else:
                        print(f"Capitão do time {time} não encontrado.")
    except Exception as e:
        print(f"Erro ao verificar e enviar emails: {e}")

def automatic_sender():
    # Configurações e dados necessários
    usuarios_csv = 'usuarios.csv'  # Caminho para o CSV dos usuários
    partidas_csv = 'partidas.csv'  # Caminho para o CSV das partidas
    remetente = 'botemailAbreu@gmail.com'  # Email do remetente
    senha = 'bkas zfdi gkif xiee'  # Senha do aplicativo

    # Executando a função para verificar e enviar emails
    try:
        verificar_e_enviar_emails(usuarios_csv, partidas_csv, remetente, senha)
    except Exception as e:
        print(f"Erro ao executar a verificação de emails: {e}")