import requests

# URL do endpoint
url = "https://publicapi.challengermode.com/mk1/v1/tournaments"
# Cabeçalhos (inclui o token Bearer)
headers = {
    "Authorization": "Bearer eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiSldULUFFUy1LRVkiLCJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QifQ.Gb4vA7bxA7eGQnos1Lgx_iwbTX893H7l9F6BQUgqRX97-DG6qVDcd6ROoyQtesaJowWPEFJoKZXfcXT6fWvJVkPQJU5k9kcr.CNb1PsyBRCkhfq_dg5la8w.XdrIysxsUE7pZmR7Nf4ArmfsFewkfGMU9C3g_1_39LbG0XwsanOz9kmD9I-X1Dh4u8xaUyySEE0ZQZFI9mYmXC3dyqc5c75SlMqtazvixo9LJRF7eFGJ6qv1QupzEG2qbUXMxuPFOMMvpKk8dIuJlVCzJsacoh92ucZq9q1n04W1esfXDFISuTR9m2jz1qy9VdxD1kz8ouhDjWqXc2v0deVXD7per9KO82OwG2AicsTIYeygpRQgN_bp92LRn7xoAaF6ED-Zv9LrCumTfM0BMAsM5MgOUWQBtsnQuCJBI0caUxFWBeG5A8xg3DGTp6ynGeiZwpz4shkmwV6kw7ESj3I-jl8GC1pYQuW8f-Unl2cKTKrl8_uGdPczRy0jiH5HuHM2H9V7fqxaDTJRDP9Em1cqAaQjO6qx4LNzIDay_quRfX5G1Qtd9AYgYZZbYswGFH7SDy8WioXsqP3XlBsHXvgU60t22q99y7o1GSZrJgYZDKDrVtD8X6mZee5u404b8B3DR2cFZVAfj8xnagKh92YoxexZT2ncWHgY4FCt9WpOTPWsZNtMEXmmmXmXTnuszy1h6ACmFWijoU8pcPuZ3ZUAkZsH0lkD0e44hEkOcbAi7sdium8NJxQupZASLVbbYS0S7JG7MvmBf1HMJNleSlYuMOIHxRobr9qOAX_cxsQv2YyJIiaF6Tphm7gb2CeD-ALVNVYtCmYYVnm4dptPmnpMoipfUDGtL_N6m9V-BxN5I_1M8e-Be_itv13FenHfiQJLEJkEy2acnOngKI51SFYrwZaD_0KKvrg0BGVvUTBKhA2sTgpa8CqsDFJZ1Pm4FTX8Fa4tzO_QYH0YKF8Hx3JUdTUrzoOGZ0S5HufYLIhlnfYWkLMfb7FEy-7D9gZ1Lmh98eDkyt0-uuDwGKR39COnxHNzxjxR2AE1su0TZQl6-8e8NnDuBxFf5Cuq8M-Xu0_DjtFJUwqa0pcO7at3zuegVa5HgedCv4Sjn8ARs99WdapHWrdYezEumSyb4EBmXvvXuJwS7BJqgOLUibnServQfP39ue-iCV7UxUhGcELpKHfO8k3Dw9wr3nIfGoF455upZHNMcbNe7GOUPeya6J5qzURsxRpHzqx5jR0YOZ4jjl6PQEkifkk8Ko6tWxj-5DbvfT0DsDqBC1BtZ9c1m3XY456yVeaF5HQa82RlIV47IFzszb69q0nYRmrhosl1iY-lkeC58c3gn11nOcdKhLFagKqVR64YC2VTBq3-6KlYenTD_7-S9XMsAfRpWR2gLiyhHVeH6LqLKOZJgWKIcC0zk36T8pkUoZUDtLmFeXhyEDKHjLvkHOgykIrs4tJ-twDSBOWG6dndQZlwOHbxNxQLH277g_7haNeoel3_DLRsg-WC5PTNFqGpeA_BBibspjgiZbOomVw8jRwYqXrD0gG8XwwyF_w7iW3vKw-snnzp26M4npqOdyqmw2-P55Q4SO8J1Qt5soNCS1lP76dSiMFbsm8zEVYnboBiW1wUcVPb77OrE1_GGFd0Ek2cwd21KeaPBkn5mE48Wod48Z8k2N5SHLn38CljFbpT7kgE4IHBGrawIDu13ZqfwLwJacyIhYYUGw2nrNmMQJ_fNLoBWgFxYZ0S0KyxN4fEYedmo52sCTz1elpxBcx0mZDfXOjv6LSK-9KAy0YC4IdGAGb6mAEQuGuyRd9iHdWgczsVipQy6Md7RGanEEK3A27-efJRbJ8D02cYuMxhYZi2tEt-M6K0vHNDisgM2I2MFYo_2GHc4dZpPjU3wJlZ4z2LUYIt.Lr4XRi8c6elV5ciH6mPq4A_7ImwIhkk3B6SE41c6Vc4"
}

# Função para obter e filtrar torneios relacionados à "AcadArena"
def get_acadarena_tournaments():
    academarena_tournaments = []
    page = 1
    while True:
        # Fazendo a requisição para a página atual
        response = requests.get(url, headers=headers, params={"page": page})
        
        # Verificando se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Convertendo a resposta para JSON
            data = response.json()

            # Se o retorno for um dicionário (caso haja apenas um torneio), lidamos com isso
            if isinstance(data, dict):
                data = [data]

            # Filtrar os torneios que tenham "AcadArena" no nome ou descrição
            for tournament in data:
                if "AcadArena" in tournament.get("name", "") or "AcadArena" in tournament.get("descriptionId", ""):
                    academarena_tournaments.append(tournament)

            # Se a quantidade de torneios na página for menor que o limite, paramos
            if len(data) < 50:
                break
            
            # Avançar para a próxima página
            page += 1
        else:
            print(f"Erro {response.status_code}: {response.text}")
            break
    
    return academarena_tournaments

# Chamando a função para obter torneios relacionados à "AcadArena"
tournaments = get_acadarena_tournaments()

# Exibindo os torneios
if tournaments:
    print(f"Torneios relacionados à 'AcadArena': {len(tournaments)}")
    for tournament in tournaments:
        print(f"Torneio: {tournament['name']}, ID: {tournament['id']}, URL: {tournament.get('overviewUrl', 'N/A')}")
else:
    print("Nenhum torneio relacionado à 'AcadArena' foi encontrado.")
