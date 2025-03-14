import pandas as pd
import random

joker = {
    "jokers" : ("pair-c", "pair-m", "three-c", "three-m", "four-c", "four-m", "straight-c", "straight-m", "flush-c", "flush-m"),
    "penis" : ['pimto','penis','trolhona','rola','cinco','6','7','8','9','10']
}

dfj = pd.DataFrame(joker)
randomjk = random.randint(0, 9)
print(dfj.at[randomjk, "jokers"])

indexm = dfj.index[dfj["jokers"] == "three-c"].tolist()

# Verifica se a lista indexm não está vazia antes de acessar o primeiro elemento
if indexm:
    print(dfj.at[indexm[0], 'penis'])
else:
    print("Nenhum índice encontrado para 'three-c'.")