import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os  # Para garantir o uso das variáveis de ambiente

def enviar_email(destinatario, nome, torneio, data_partida, horario_partida, time, cargo, remetente, senha):
    try:
        # Verificar se os campos são válidos
        if not destinatario or not remetente or not senha:
            raise ValueError("Destinatário, remetente ou senha não foram fornecidos corretamente.")

        # Configuração do servidor SMTP (exemplo: Gmail)
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remetente, senha)

        # Criação do email
        email = MIMEMultipart()
        email['From'] = remetente
        email['To'] = destinatario
        email['Subject'] = f"Confirmação da Partida do {torneio} em {data_partida}"

        # Mensagem personalizada com HTML para formatação
        mensagem = f"""
        <html>
            <body>
                <p>Olá {nome},</p>
                <p>Esta é a confirmação oficial da sua próxima partida pelo torneio <strong>{torneio}</strong>.</p>
                <ul>
                    <li><strong>Time:</strong> {time}</li>
                    <li><strong>Cargo:</strong> {cargo}</li>
                    <li><strong>Data:</strong> {data_partida}</li>
                    <li><strong>Horário:</strong> {horario_partida}</li>
                </ul>
                <p>Por favor, confirme sua presença o mais breve possível através do formulário:</p>
                <p><a href="https://forms.gle/exemplo">Clique aqui para confirmar</a></p>
                <p>Sua confirmação é muito importante para a organização do evento.</p>
                <p>Atenciosamente,<br>Organização do Evento</p>
            </body>
        </html>
        """

        email.attach(MIMEText(mensagem, 'html'))  # Enviar como HTML

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

        # Converter ID para string e remover NaNs
        participantes['ID'] = participantes['ID'].astype(str)
        participantes = participantes.dropna(subset=['ID', 'Nome Completo', 'E-mail', 'Time', 'Cargo (Capitão ou jogador)'])

        # Filtrar linhas de teste ou inválidas
        participantes = participantes[~participantes['ID'].str.lower().str.contains('teste')]
        participantes = participantes[~participantes['Nome Completo'].str.lower().str.contains('teste')]

        participante_id = str(participante_id)

        # Filtra o participante pelo ID
        participante = participantes[participantes['ID'] == participante_id]

        if not participante.empty:
            time_participante = participante.iloc[0]['Time']
            email = participante.iloc[0]['E-mail']
            cargo = participante.iloc[0]['Cargo (Capitão ou jogador)']
            nome = participante.iloc[0]['Nome Completo']

            # Filtra a partida relevante para o time do participante
            partida = partidas[
                (partidas['time1'] == time_participante) | (partidas['time2'] == time_participante)
            ]

            if not partida.empty:
                data_partida = partida.iloc[0]['data_partida']
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
            print(f"Participante com ID {participante_id} não encontrado.")
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Erro: Arquivo CSV vazio - {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
