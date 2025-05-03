import random
import pandas as pd

import tabelas

# DataFrame for poker hands

df = tabelas.df

dfp = tabelas.dfp

print(f'{df}\n {dfp}')

class Joker:
    def __init__(self, nome, legendary_jokers, efeito):
        self.nome= nome
        self.legendary_jokers = legendary_jokers
        self.efeito = efeito

    def __str__(self):
        return f"Joker: {(self.jokers)}, Legendary Jokers: {(self.legendary_jokers)}"

class Planetarium:
    def __init__(self, planetaescolhido):
        #se transforma em uma carta baseado no número dado
        self.nome       = dfp.at[planetaescolhido, 'Nome_Carta']
        self.mao_buff   = dfp.at[planetaescolhido, 'Buff_hand']
        self.chips      = dfp.at[planetaescolhido, 'Aumento_chips']
        self.mult       = dfp.at[planetaescolhido, 'Aumento_mult']
        

    def use(self):
            print(f'dando um buff para a mão: {self.mao_buff}')

            df.loc[df['Nome da mão']== self.mao_buff, 'Chips'] += self.chips
            df.loc[df['Nome da mão']== self.mao_buff, 'Mult'] += self.mult     
            





class Shop:
    def __init__(self):
        self.planetarium_chance = 0.75  # 75% chance
        self.joker_chance = 0.25  # 25% chance
        self.shitem = []

    def reroll(self):
        self.shitem = []  # Clear previous items

        # Randomly choose one Joker based on its chance
        if random.random() < self.joker_chance:
            self.shitem.append(Joker(range(1, 17), range(1, 6)))  # Create an instance of Joker

        # Randomly choose one Planetarium based on its chance
        if random.random() < self.planetarium_chance:
            qual_carta=random.randint(0,8)
            print(f"carta planetário escolhida: {dfp.at[qual_carta,'Nome_Carta']}")
            self.shitem.append(dfp.at[qual_carta,'Nome_Carta'])

        # If neither is selected, you can choose to add a message or leave it empty
        if not self.shitem:
            self.shitem.append("Sem itens na loja")  # Optional: indicate no items

    def display_shop(self):
        """Loja Atual"""
        print("Loja Renovada")
        for item in self.shitem:
            print(f"- {item} -")  # Display the string representation of the item
'''
# Example usage
shop = Shop()
for _ in range(3):
    shop.reroll() 
    shop.display_shop() 
    print()  # Print a newline for better readability'
'''