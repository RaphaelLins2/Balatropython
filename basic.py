import random
import pandas as pd
import pygame

# Tabela de pontuação
data = {
    'Nome da mão': ['Carta Alta', 'Par', 'Dois Par', 'Trinca', 'Sequência', 'Flush', 'Full House', 'Quadra', 'Flush em sequência'],
    'Chips': [5, 10, 20, 30, 30, 35, 40, 60, 100],
    'Mult': [1, 2, 2, 3, 4, 4, 4, 7, 8]
}
df = pd.DataFrame(data)
print(df)
# Criando uma classe de cartas
class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __str__(self):
        value_str = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}.get(self.value, str(self.value))
        return f'{value_str}{self.color}'

naipes_prioridade = {'♥': 4, '♦': 3, '♣': 2, '♠': 1}
colors = ['♥', '♦', '♣', '♠']

deck = [Card(value, color) for value in range(1, 14) for color in colors]
hand = []
pontuacao = 0
nivel = 1
pontuacao_necessaria = 300

# Configurações da mão
tamanho_mao = 8
tamanho_mao_atual = 0
maos_jogadas = 0
maos_descartadas = 0
limite_maos = 4
limite_descartes = 3

def fill_hands():
    global tamanho_mao_atual
    while tamanho_mao_atual < tamanho_mao and deck:
        card = deck.pop(0)
        hand.append(card)
        tamanho_mao_atual += 1

def ordenar_mao():
    hand.sort(key=lambda carta: (-carta.value, -naipes_prioridade[carta.color]))

def print_hand():
    ordenar_mao()
    print(f"cartas no deck: {len(deck)}")
    print(f"\nNível: {nivel}, Pontos: {pontuacao}/{pontuacao_necessaria}")
    print(f"Mãos a jogar: {limite_maos - maos_jogadas}, Mãos de descarte: {limite_descartes - maos_descartadas}")
    print("Cartas em mão:")
    for i, card in enumerate(hand):
        print(f"{i + 1}. {card}")

def embaralhar():
    random.shuffle(deck)

def fichas_das_cartas(cartas):
    valores_cartas = {1: 11, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 10, 12: 10, 13: 10}
    total_fichas = sum(valores_cartas[card.value] for card in cartas)
    return total_fichas


def avaliar_mao(cartas):
    valores = sorted([carta.value for carta in cartas])
    naipes = [carta.color for carta in cartas]
    
    contagem_valores = {v: valores.count(v) for v in set(valores)}
    contagem_naipes = {n: naipes.count(n) for n in set(naipes)}
    
    tem_flush = any(count >= 5 for count in contagem_naipes.values())
    tem_sequencia = any(valores[i:i+5] == list(range(valores[i], valores[i]+5)) for i in range(len(valores)-4))
    
    if tem_flush and tem_sequencia:
        return 'Flush em sequência'
    elif 4 in contagem_valores.values():
        return 'Quadra'
    elif sorted(contagem_valores.values()) == [2, 3]:
        return 'Full House'
    elif tem_flush:
        return 'Flush'
    elif tem_sequencia:
        return 'Sequência'
    elif 3 in contagem_valores.values():
        return 'Trinca'
    elif list(contagem_valores.values()).count(2) == 2:
        return 'Dois Par'
    elif 2 in contagem_valores.values():
        return 'Par'
    else:
        return 'Carta Alta'

# --------------------------------- Jogo ---------------------------------
embaralhar()
fill_hands()

while True:
    print_hand()
    while True:
        cartas_para_selecionar = input("Selecione as cartas (separando por vírgula): ")
        cartas_para_selecionar = [int(x.strip()) - 1 for x in cartas_para_selecionar.split(',')]
        if len(cartas_para_selecionar) <=5:
            break
        else:
            input(f"\nMão não pode ter mais que 5 cartas!\nPressione Enter para continuar")
    if any(i < 0 or i >= len(hand) for i in cartas_para_selecionar):
        input("\nSeleção inválida! Por favor, selecione índices válidos.\nPressione Enter para continuar")
        continue
    
    cartas_para_remover = [hand[i] for i in sorted(cartas_para_selecionar, reverse=True)]
    nome_mao = avaliar_mao(cartas_para_remover)
    row = df[df['Nome da mão'] == nome_mao]
    chips = row['Chips'].values[0]
    mult = row['Mult'].values[0]
    chips_mao = fichas_das_cartas(cartas_para_remover)

    print(f"\n[{nome_mao}]: fichas: {chips} x {mult} Multiplicador")
    while True:
        jogar_ou_descarte = input("Você quer Jogar (J) ou Descartar (D) todas as cartas selecionadas? ").upper()
        if jogar_ou_descarte not in ["J", "D"]:
            input("\nOpção inválida. Selecione apenas (J) ou (D)\nPressione Enter para continuar")
        else:
            break
    
    if jogar_ou_descarte == "D" and maos_descartadas < limite_descartes:
        print("Você descartou as cartas.")
        maos_descartadas += 1
    elif jogar_ou_descarte == "J":
        pontos_ganhos = (chips_mao+chips) * mult
        pontuacao += pontos_ganhos
        print(f"Você ganhou {pontos_ganhos} pontos!")
        maos_jogadas += 1
    else:
        input("\nVocê não tem mais descartes, Jogue uma mão!\nPressione Enter para continuar")
        
    
    for carta in cartas_para_remover:
        hand.remove(carta)
        tamanho_mao_atual -= 1
    
    fill_hands()
    
    if pontuacao >= pontuacao_necessaria:
        nivel += 1
        pontuacao_necessaria +=50
        pontuacao = 0
        maos_jogadas = 0
        maos_descartadas = 0
        upgrade = 5
        print(f"\nParabéns! Você subiu para o nível {nivel}!\n agora sua recompensa:")
        match upgrade:
            case 1:
                limite_maos +=1
                print("Drop comum\nSeu limite de mãos foi aumentado!")
            case 2:
                limite_descartes +=1
                print("Drop comum\nSeu limite de descartes foi aumentado!")
            case 3:
                tamanho_mao +=1
                print("Drop comum\nSeu Tamanho de mão foi aumentado!")
            case 4:
                print("Drop comum\nVocê não ganhou nenhum upgrade :(")
            case 5:
                while True:
                    gambling = str(input("Drop raro!!!! \nVocê tem duas escolhas:\n1°: Uma chanche de 1 em 6 de ganhar um upgrade de 2 pontos pra todos os seus status\n2°: Ou descer para um nível mais fácil \n(1/2):"))
                    if gambling == "1":
                        print("Certo! Pressione Enter para girar o dado")
                        dado = random.randint(1,6)
                        if dado == 6:
                            print("parabéns você teve um upgrade total!!!")
                            limite_maos +=2
                            limite_descartes +=2
                            tamanho_mao +=2
                            break
                        else:
                            print("Ops, não foi dessa vez")
                            break
                    elif gambling == "2":
                        print("então tá, indo um level a menos agora!")
                        nivel-=2
                        pontuacao_necessaria-=100
                        break
        
        input("Pressione enter para continuar")
        deck = [Card(value, color) for value in range(1, 14) for color in colors]
        for i in range(len(hand)):
            hand.pop(i)
        embaralhar
        
    if maos_jogadas >= limite_maos :
        break

    

print(f"\nFim da partida! Nível alcançado: {nivel}, Pontuação final: {pontuacao}")
