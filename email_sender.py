import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def enviar_email(destinatario, nome, torneio, data_partida, horario_partida, time, cargo, remetente, senha):
    try:
        # Configuração do servidor SMTP (exemplo: Gmail)
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remetente, senha)

        # Criação do email
        email = MIMEMultipart()
        email['From'] = remetente
        email['To'] = destinatario
        email['Subject'] = f"Confirmação da Partida do {torneio} em {data_partida}"

        # Mensagem personalizada
        mensagem = f"""
        Olá {nome},

        Esta é a confirmação oficial da sua próxima partida pelo torneio **{torneio}**.

        *Informações da Partida:*
        - Time: {time}
        - Cargo: {cargo}
        - Data: {data_partida}
        - Horário: {horario_partida}

        *Por favor, confirme sua presença o mais breve possível* através do formulário:

        *Google Forms*: [Clique aqui para confirmar](https://forms.gle/exemplo)

        Sua confirmação é muito importante para a organização do evento.

        Atenciosamente,
        Organização do Evento
        """

        email.attach(MIMEText(mensagem, 'plain'))

        # Enviando o email
        servidor.sendmail(remetente, destinatario, email.as_string())
        print(f"Email enviado para {destinatario}")

        servidor.quit()
    except Exception as e:
        print(f"Erro ao enviar email para {destinatario}: {str(e)}")

def buscar_e_enviar_email(participante_id, participantes_csv, partidas_csv, remetente, senha):
    try:
        # Lendo os arquivos CSV
        participantes = pd.read_csv(participantes_csv, encoding='utf-8')
        partidas = pd.read_csv(partidas_csv, encoding='utf-8')

        # Filtra o participante pelo id
        participante = participantes[participantes['id'] == participante_id]

        if not participante.empty:
            time_participante = participante.iloc[0]['time']
            email = participante.iloc[0]['email']
            cargo = participante.iloc[0]['cargo']
            nome = participante.iloc[0]['nome']

            # Filtra a partida relevante para o time do participante
            partida = partidas[
                (partidas['time1'] == time_participante) | (partidas['time2'] == time_participante)
            ]

            if not partida.empty:
                data_partida = datetime.strptime(partida.iloc[0]['data_partida'], '%Y-%m-%d').date()
                horario_partida = partida.iloc[0]['horario_partida']
                torneio = partida.iloc[0]['torneio']

                # Envia o email
                enviar_email(
                    email, nome, torneio, data_partida, horario_partida,
                    time_participante, cargo, remetente, senha
                )
            else:
                print(f"Partida não encontrada para o time {time_participante}.")
        else:
            print(f"Participante com id {participante_id} não encontrado.")
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Erro: Arquivo CSV vazio - {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
