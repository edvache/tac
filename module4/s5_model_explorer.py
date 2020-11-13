"""Playing with word2vec model"""

#%%
from gensim.models import Word2Vec
from pprint import pprint

model = Word2Vec.load("data/bulletins.model")

word1 = "boucher"
pprint(model.wv[word1])

#%%
word2 = "fleuriste"
sim1 = model.wv.similarity(word1, word2)
print(f"{word1} is {100*sim1:.1f}% similar to {word2}\n")

#%%
word2 = "boulanger"
sim1 = model.wv.similarity(word1, word2)
print(f"{word1} is {100*sim1:.1f}% similar to {word2}\n")

#%%
pprint(model.wv.most_similar("kermesse", topn=3))

#%%
pprint(model.wv.most_similar("bruxelles"))

#%%
pprint(model.wv.most_similar(positive=['bruxelles', 'france'], negative=['belgique']))


print("\nMots que j'ai choisi\n")

myWord_1 = "route"
pprint(model.wv[myWord_1])

myWord_2 = "chemin"
first_similarity = model.wv.similarity(myWord_1, myWord_2)
print(f"{myWord_1} is {100*first_similarity:.1f}% similar to {myWord_2}\n")

myWord_3 = "autoroute"
second_similarity = model.wv.similarity(myWord_1, myWord_3)
print(f"{myWord_1} is {100*second_similarity:.1f}% similar to {myWord_3}\n")


myWord_4 = "bière"
pprint(model.wv[myWord_1])

myWord_5 = "gaufres"
first_similarity = model.wv.similarity(myWord_4, myWord_5)
print(f"{myWord_4} is {100*first_similarity:.1f}% similar to {myWord_5}\n")

myWord_6 = "frites"
second_similarity = model.wv.similarity(myWord_4, myWord_6)
print(f"{myWord_4} is {100*second_similarity:.1f}% similar to {myWord_6}\n")

myWord_7 = "université"
pprint(model.wv[myWord_1])

myWord_8 = "maternelle"
first_similarity = model.wv.similarity(myWord_7, myWord_8)
print(f"{myWord_7} is {100*first_similarity:.1f}% similar to {myWord_8}\n")

myWord_9 = "secondaire"
second_similarity = model.wv.similarity(myWord_7, myWord_9)
print(f"{myWord_7} is {100*second_similarity:.1f}% similar to {myWord_9}\n")

print("Mot choisi --> artisan, affichant les 5 premiers résultats")
pprint(model.wv.most_similar("artisan", topn=5))

print("\nMot choisi --> marché")
pprint(model.wv.most_similar("marché"))

print("\nPositive --> Maison et Campagne | Negative --> Ville")
pprint(model.wv.most_similar(positive=['maison', 'campagne'], negative=['ville']))
