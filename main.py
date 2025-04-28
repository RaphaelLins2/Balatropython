#importando todas as bibliotecas necessárias para o código
import random
import pandas as pd
import colorama
from colorama import Fore, Back, Style

colorama.init()

# Tabela de pontuação
data = {
    'Nome da mão': ['Carta Alta', 'Par', 'Dois Par', 'Trinca', 'Sequência', 'Flush', 'Full House', 'Quadra', 'Flush em sequência'],
    'Chips': [5, 10, 20, 30, 30, 35, 40, 60, 100],
    'Mult': [1, 2, 2, 3, 4, 4, 4, 7, 8]
}
df = pd.DataFrame(data)

#tabela de cores para cada naipe
color_map = {
    '♥': Fore.RED,
    '♦': Fore.YELLOW,
    '♣': Fore.BLUE,
    '♠': Fore.WHITE  # Mantendo branco porque preto pode não ser visível em terminais escuros
}

print(df)
# Criando uma classe de cartas
class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __str__(self):
        value_str = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}.get(self.value, str(self.value))
        return f"{color_map[self.color]}{value_str}{self.color}{Style.RESET_ALL}"

#criando as prioridades para a organização do deck
naipes_prioridade = {'♥': 4, '♦': 3, '♣': 2, '♠': 1}
colors = ['♥', '♦', '♣', '♠']

#iniciando variaveis de:
#deck/cartas
deck = [Card(value, color) for value in range(1, 14) for color in colors]
hand = []
cartas_descartadas = []
#nivel / pontuação
pontuacao = 0
nivel = 1
pontuacao_necessaria = 300
#configurações da mão
tamanho_mao = 8
tamanho_mao_atual = 0
maos_jogadas = 0
maos_descartadas = 0
limite_maos = 4
limite_descartes = 3

def fill_hands():
    #função para encher a mão
    global tamanho_mao_atual
    while tamanho_mao_atual < tamanho_mao and deck:
        #removendo as cartas do deck e colocando elas na mão(adicionando ao tamanho da mão atual total)
        card = deck.pop(0)
        hand.append(card)
        tamanho_mao_atual += 1

def ordenar_mao():
    #algoritimo para ordernar a mão corretamente
    hand.sort(key=lambda carta: (-carta.value, -naipes_prioridade[carta.color]))

def print_hand():
    #função para mostrar a mão formatada de maneira bonitinha 
    #junto com o header do jogo contendo informações sobre a run
    ordenar_mao()
    print(f"cartas no deck: {len(deck)}")
    print(f"\nNível: {nivel}, Pontos: {pontuacao}/{pontuacao_necessaria}")
    print(f"Mãos a jogar: {limite_maos - maos_jogadas}, Mãos de descarte: {limite_descartes - maos_descartadas}")
    print("Cartas em mão:")
    #enumerador das cartas
    for i, card in enumerate(hand):
        print(f"{i + 1}. {card}")

def embaralhar():
    #uao o que será que a função embaralhar faz né?
    random.shuffle(deck)

def fichas_das_cartas(cartas):
    #diz o que cada carta ira dar em fichas durante a pontuação
    #(Posteriormente deverá ser adicionado uma função para adicionar multiplicador também)
    valores_cartas = {1: 11, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 10, 12: 10, 13: 10}
    total_fichas = sum(valores_cartas[card.value] for card in cartas)
    return total_fichas

def avaliar_mao(cartas):
    #genuinamente eu não sei como funciona muito bem mas eu sei que isso aqui faz um bom trabalho
    #em avaliar qual mão você está jogando de forma linear(melhor mão-->pior mão)
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

def selecionador():
    #script para selecionar as cartas que estão na sua mão
    while True:
            global cartas_para_selecionar
            cartas_para_selecionar = input("Selecione as cartas (separando por vírgula): ")
            cartas_para_selecionar = [int(x.strip()) - 1 for x in cartas_para_selecionar.split(',')]
            if len(cartas_para_selecionar) <=5:
                break
            else:
                input(f"\nMão não pode ter mais que 5 cartas!\nPressione Enter para continuar")
    if any(i < 0 or i >= len(hand) for i in cartas_para_selecionar):
            input("\nSeleção inválida! Por favor, selecione índices válidos.\nPressione Enter para continuar")

def oqfazercomcartas():
    #decide o que faz com as cartas

    #importando as variaveis necessárias para o script funcionar
    global cartas_para_remover
    global chips
    global mult
    global chips_mao
    global nome_mao

    global pontuacao
    global maos_jogadas
    global maos_descartadas

    global tamanho_mao_atual

    global cartas_descartadas

    #lê e informa todas as informações sobre a mão que foi jogada
    cartas_para_remover = [hand[i] for i in sorted(cartas_para_selecionar, reverse=True)]
    nome_mao = avaliar_mao(cartas_para_remover)
    row = df[df['Nome da mão'] == nome_mao]
    chips = row['Chips'].values[0]
    mult = row['Mult'].values[0]
    chips_mao = fichas_das_cartas(cartas_para_remover)

    print(f"\n[{nome_mao}]: fichas: {chips} x {mult} Multiplicador")
    while True: #loop principal para decidir o que será feito com a mão (pode escolher entre jogar ou descartar)
        jogar_ou_descarte = input("Você quer Jogar (J) ou Descartar (D) todas as cartas selecionadas? ").upper()
        if jogar_ou_descarte not in ["J", "D"]:
            input("\nOpção inválida. Selecione apenas (J) ou (D)\nPressione Enter para continuar")
        elif jogar_ou_descarte == "D" and maos_descartadas < limite_descartes:
            print("Você descartou as cartas.")
            maos_descartadas += 1
            break
        elif jogar_ou_descarte == "J":
            pontos_ganhos = (chips_mao+chips) * mult
            pontuacao += pontos_ganhos
            print(f"Você ganhou {pontos_ganhos} pontos!")
            maos_jogadas += 1
            break
        else:
            input("\nVocê não tem mais descartes, Jogue uma mão!\nPressione Enter para continuar")
    
    for carta in cartas_para_remover: # remove as cartas da mão jogada ou descartada e coloca na pilha de descartes
            cartas_descartadas.append(carta)
            hand.remove(carta)
            tamanho_mao_atual -= 1

def ganhou():
    #script que decide o que vai ocorrer quando for passado de nivél   
    #no momento ele está bem ruim, posteriormente quando o sistema de loja for implementado
    #todo o código nessa função vai ser bem obsoleto

    #chamando variáveis
    global nivel
    global pontuacao_necessaria
    global pontuacao
    global maos_jogadas
    global maos_descartadas
    global limite_descartes
    global limite_maos
    global tamanho_mao
    global cartas_descartadas

    global hand
    global tamanho_mao_atual

    #formatando essas variáveis para a passagem de nível
    nivel += 1
    pontuacao_necessaria +=50
    pontuacao = 0
    maos_jogadas = 0
    maos_descartadas = 0
    upgrade = random.randint(1,5)
    print(f"\nParabéns! Você subiu para o nível {nivel}!\nagora sua recompensa:")
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
    #coloca todas as cartas que antes foram descartadas de volta no deck e então o embaralha
    for item in cartas_descartadas:
        deck.append(item)
    embaralhar()
    hand = []
    tamanho_mao_atual = 0
    fill_hands()
    
# --------------------------------- Jogo ---------------------------------
def jogo():
    #chamando praticamente todas variáveis dessa maneira por preguiça de uma maneira melhor praticamente
    global hand
    global pontuacao
    global pontuacao_necessaria
    global maos_descartadas
    global maos_jogadas
    global limite_maos
    global limite_descartes
    global nivel
    global tamanho_mao
    global tamanho_mao_atual
    embaralhar()
    fill_hands()

    #loop principal do jogo
    while True:
        print_hand()
        
        selecionador()
        
        oqfazercomcartas()

        fill_hands()
        
        if pontuacao >= pontuacao_necessaria:
            ganhou()
            
        if maos_jogadas >= limite_maos :
            #fechando o loop para dizer que o player perdeu
            break

    print(f"\nFim da partida! Nível alcançado: {nivel}, Pontuação final: {pontuacao}")
jogo()