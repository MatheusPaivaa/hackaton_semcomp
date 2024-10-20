import csv

def preencher_ids(csv_input, csv_output):
    # Lista para armazenar os dados atualizados
    dados_atualizados = []
    ids_existentes = set()
    max_id = 0

    # Nome da coluna ID no seu CSV
    nome_campo_id = 'ID'  # Atualize se o nome da coluna for diferente

    # Primeiro, lemos o arquivo CSV e coletamos os IDs existentes
    with open(csv_input, mode='r', encoding='utf-8') as csvfile:
        leitor = csv.DictReader(csvfile)
        campos = leitor.fieldnames  # Obter os nomes das colunas

        for linha in leitor:
            id_atual = linha[nome_campo_id].strip()
            if id_atual and id_atual.lower() != 'teste':
                try:
                    id_num = int(id_atual)
                    ids_existentes.add(id_num)
                    if id_num > max_id:
                        max_id = id_num
                except ValueError:
                    # Caso o ID não seja um número válido, ignoramos
                    pass
            dados_atualizados.append(linha)

    # Agora, percorremos os dados e preenchemos os IDs vazios ou inválidos
    novo_id = max_id + 1
    for linha in dados_atualizados:
        id_atual = linha[nome_campo_id].strip()
        if not id_atual or id_atual.lower() == 'teste':
            while novo_id in ids_existentes:
                novo_id += 1  # Garante que o ID é único
            linha[nome_campo_id] = str(novo_id)
            ids_existentes.add(novo_id)
            novo_id += 1

    # Escrevemos os dados atualizados em um novo arquivo CSV
    with open(csv_output, mode='w', newline='', encoding='utf-8') as csvfile:
        escritor = csv.DictWriter(csvfile, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(dados_atualizados)

    print(f"IDs vazios foram preenchidos e o arquivo '{csv_output}' foi atualizado.")

# Exemplo de uso:
csv_input = 'usuarios.csv'     # Nome do arquivo CSV de entrada
csv_output = 'usuarios.csv'    # Nome do arquivo CSV de saída (pode ser o mesmo para sobrescrever)

preencher_ids(csv_input, csv_output)
