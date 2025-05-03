import pandas as pd

data = {
    'Nome da mão': ['Carta Alta', 'Par', 'Dois Par', 'Trinca', 'Sequência', 'Flush', 'Full House', 'Quadra', 'Flush em sequência'],
    'Chips': [5, 10, 20, 30, 30, 35, 40, 60, 100],
    'Mult': [1, 2, 2, 3, 4, 4, 4, 7, 8]
}
df = pd.DataFrame(data)


Planetas = {
    'Nome_Carta'    :   ['pluto', 'mercury', 'uranus','venus','saturno','jupiter','earth','mars','neptune'],
    'Buff_hand'     :   ['Carta Alta', 'Par', 'Dois Par', 'Trinca', 'Sequência', 'Flush', "Full House", 'Quadra', 'Flush em sequência'],
    
    'Aumento_chips' :   [10,15,20,20,30,15,25,30,40],
    'Aumento_mult'  :   [1,1,1,2,3,2,2,3,4]
}
dfp = pd.DataFrame(Planetas)


