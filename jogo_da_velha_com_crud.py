import json
import os

ARQUIVO = 'partidas.json'

def carregar_partidas():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r') as f:
        return json.load(f)

def salvar_partidas(partidas):
    with open(ARQUIVO, 'w') as f:
        json.dump(partidas, f, indent=4)

def criar_partida():
    partida = {
        "id": len(carregar_partidas()) + 1,
        "tabuleiro": [" "]*9,
        "jogador_atual": "X",
        "finalizada": False
    }
    partidas = carregar_partidas()
    partidas.append(partida)
    salvar_partidas(partidas)
    print(f"Partida criada com ID {partida['id']}.")

def listar_partidas():
    partidas = carregar_partidas()
    if not partidas:
        print("Nenhuma partida encontrada.")
        return
    for p in partidas:
        status = "Finalizada" if p["finalizada"] else "Em andamento"
        print(f"ID: {p['id']} | Jogador: {p['jogador_atual']} | Status: {status}")

def deletar_partida():
    idp = int(input("ID da partida para deletar: "))
    partidas = carregar_partidas()
    novas = [p for p in partidas if p["id"] != idp]
    if len(novas) == len(partidas):
        print("ID não encontrado.")
    else:
        salvar_partidas(novas)
        print("Partida removida.")

def mostrar_tabuleiro(tabuleiro):
    print()
    for i in range(3):
        print(" | ".join(tabuleiro[i*3:(i+1)*3]))
        if i < 2:
            print("--+---+--")
    print()

def checar_vitoria(tabuleiro):
    combinacoes = [
        [0,1,2],[3,4,5],[6,7,8], # linhas
        [0,3,6],[1,4,7],[2,5,8], # colunas
        [0,4,8],[2,4,6]          # diagonais
    ]
    for c in combinacoes:
        if tabuleiro[c[0]] == tabuleiro[c[1]] == tabuleiro[c[2]] != " ":
            return True
    return False

def jogar_partida():
    idp = int(input("ID da partida para jogar/continuar: "))
    partidas = carregar_partidas()
    partida = next((p for p in partidas if p["id"] == idp), None)
    if not partida:
        print("Partida não encontrada.")
        return
    if partida["finalizada"]:
        print("Essa partida já foi finalizada.")
        return

    while True:
        mostrar_tabuleiro(partida["tabuleiro"])
        pos = int(input(f"Jogador {partida['jogador_atual']}, escolha posição (1-9): ")) - 1
        if pos < 0 or pos > 8 or partida["tabuleiro"][pos] != " ":
            print("Posição inválida.")
            continue
        partida["tabuleiro"][pos] = partida["jogador_atual"]
        if checar_vitoria(partida["tabuleiro"]):
            mostrar_tabuleiro(partida["tabuleiro"])
            print(f"Jogador {partida['jogador_atual']} venceu!")
            partida["finalizada"] = True
            break
        elif " " not in partida["tabuleiro"]:
            mostrar_tabuleiro(partida["tabuleiro"])
            print("Empate!")
            partida["finalizada"] = True
            break
        partida["jogador_atual"] = "O" if partida["jogador_atual"] == "X" else "X"

    # Atualiza a partida no arquivo
    for i, p in enumerate(partidas):
        if p["id"] == idp:
            partidas[i] = partida
            break
    salvar_partidas(partidas)

def menu():
    while True:
        print("\n--- Jogo da Velha com CRUD ---")
        print("1. Criar nova partida")
        print("2. Listar partidas")
        print("3. Jogar/Continuar partida")
        print("4. Deletar partida")
        print("5. Sair")
        op = input("Escolha uma opção: ")
        if op == '1':
            criar_partida()
        elif op == '2':
            listar_partidas()
        elif op == '3':
            jogar_partida()
        elif op == '4':
            deletar_partida()
        elif op == '5':
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()