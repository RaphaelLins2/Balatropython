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

# Inicialização do Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Cartas")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)

# Criando uma classe de cartas
class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.selected = False

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

def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_hand():
    screen.fill(WHITE)
    draw_text(f"Nível: {nivel}, Pontos: {pontuacao}/{pontuacao_necessaria}", 20, 20)
    draw_text(f"Mãos a jogar: {limite_maos - maos_jogadas}", 20, 50)
    draw_text(f"Descartes restantes: {limite_descartes - maos_descartadas}", 20, 80)
    
    y_offset = 120
    for i, card in enumerate(hand):
        color = GREEN if card.selected else BLACK
        draw_text(f"{i + 1}. {card}", 50, y_offset, color)
        y_offset += 40

    pygame.draw.rect(screen, RED, (50, 500, 150, 50))
    draw_text("Descartar", 70, 515, WHITE)

    pygame.draw.rect(screen, BLUE, (250, 500, 150, 50))
    draw_text("Jogar Mão", 270, 515, WHITE)

    pygame.display.flip()

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

# Inicialização
random.shuffle(deck)
fill_hands()
running = True

while running:
    draw_hand()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 50 <= x <= 200 and 500 <= y <= 550:  # Botão de descarte
                if maos_descartadas < limite_descartes:
                    maos_descartadas += 1
                    fill_hands()
            elif 250 <= x <= 400 and 500 <= y <= 550:  # Botão de jogar mão
                nome_mao = avaliar_mao(hand)
                row = df[df['Nome da mão'] == nome_mao]
                chips = row['Chips'].values[0]
                mult = row['Mult'].values[0]
                pontuacao += chips * mult
                maos_jogadas += 1
                hand.clear()
                fill_hands()

                if pontuacao >= pontuacao_necessaria:
                    nivel += 1
                    pontuacao_necessaria += 50
                    pontuacao = 0
                    draw_text(f"Parabéns! Você subiu para o nível {nivel}!", 300, 300, GREEN)
                    pygame.display.flip()
                    pygame.time.wait(2000)

                if maos_jogadas >= limite_maos:
                    running = False

            # Seleção de cartas
            for i, card in enumerate(hand):
                if 50 <= x <= 200 and 120 + i * 40 <= y <= 160 + i * 40:  # Verifica se clicou em uma carta
                    card.selected = not card.selected  # Alterna a seleção da carta

    clock.tick(30)

pygame.quit()
