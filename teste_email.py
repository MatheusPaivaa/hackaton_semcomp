from email_sender import buscar_e_enviar_email

# Configurações e dados necessários para o envio de email
usuarios_csv = '/home/gabriel/Documentos/Hackaton/usuarios.csv'  # Caminho para o CSV dos usuários
partidas_csv = '/home/gabriel/Documentos/Hackaton/partidas.csv'  # Caminho para o CSV das partidas
remetente = 'botemailAbreu@gmail.com'  # Email do remetente
senha = 'irsb tchk dwhz zuyd'  # Senha do aplicativo

# ID do participante para o teste
id_participante_teste = 227236575  # Alterar para um ID existente no CSV de usuários

# Executando a função para enviar email diretamente
try:
    buscar_e_enviar_email(id_participante_teste, usuarios_csv, partidas_csv, remetente, senha)
except Exception as e:
    print(f"Erro ao enviar email: {e}")
