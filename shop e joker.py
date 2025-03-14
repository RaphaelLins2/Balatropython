import random
import pandas as pd

# DataFrame for poker hands
geral = {
    'Nome da mão': ['Carta Alta', 'Par', 'Dois Par', 'Trinca', 'Sequência', 'Flush', "Full House", 'Quadra', 'Flush em sequência'],
    'Chips': [5, 10, 20, 30, 30, 35, 40, 60, 100],
    'Mult': [1, 2, 2, 3, 4, 4, 4, 7, 8]
}
df = pd.DataFrame(geral)

Planetarium = {
    'Nome_Carta' : ['pluto', 'mercury', 'uranus','venus','saturno','jupiter','earth','mars','neptune'],
    'Aumento_chips' : [10,15,20,20,30,15,25,30,40],
    'Aumento_mult' : [1,1,1,2,3,2,2,3,4]
}
dfp = pd.DataFrame(Planetarium)

print(f'{df}\n {dfp}')
class Joker:
    def __init__(self, jokers, legendary_jokers):
        self.jokers = jokers
        self.legendary_jokers = legendary_jokers

    def __str__(self):
        return f"Joker: {(self.jokers)}, Legendary Jokers: {(self.legendary_jokers)}"

class Planetarium:
    def __init__(self, pluto, mercury, venus, mars, saturn, jupiter, earth, neptune):
        self.pluto = pluto
        self.mercury = mercury
        self.venus = venus
        self.mars = mars
        self.saturn = saturn
        self.jupiter = jupiter
        self.earth = earth
        self.neptune = neptune

    def __str__(self):
        return (f"Planetarium: Pluto: {self.pluto}, Mercury: {self.mercury}, "
                f"Venus: {self.venus}, Mars: {self.mars}, Saturn: {self.saturn}, "
                f"Jupiter: {self.jupiter}, Earth: {self.earth}, Neptune: {self.neptune}")

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

# Example usage
shop = Shop()
for _ in range(3):
    shop.reroll() 
    shop.display_shop() 
    print()  # Print a newline for better readability