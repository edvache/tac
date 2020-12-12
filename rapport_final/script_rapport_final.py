"""FINAL REPORT"""

import os
import nltk
import sys
import spacy
from nltk.corpus import stopwords
from pprint import pprint
from collections import defaultdict
from spacy.lang.fr.examples import sentences
from gensim.models import Word2Vec

model = Word2Vec.load("data/bulletins.model")

nlp = spacy.load('fr_core_news_sm')
nlp.max_length = 7000000
print("--> EXTRACT FILE NAME CONTAINING LEXICON WORD")

data_path = "data/txt/"
files = os.listdir(data_path)

my_lexique = set(["végétation", "jardin", "jardins", "parc", "parcs", "arbre", "arbres", "espace vert", "écosystème",
                "biodiversité", "plante", "plantes", "jardinier", "planter",
                "bois", "forêt", "forêts", "nature", "végétaliser", "horticulture"])
print("\n--> LEXIQUE")
pprint(my_lexique)

fileName = []
i = 1
for f in sorted(files):
    i = i +1
    text = open(data_path + f, encoding='utf-8').read()
    for elem in my_lexique:
        if elem in text:
            if f not in fileName:
                fileName.append(f)

print("\n--> FILE NAME COUNT")
pprint(f"{len(fileName)} contains one or more words of our lexicon.")
print("\n--> FILE NAME LIST")
pprint(fileName)

print("\n--> ANALYSE FREQUENCY DISTRIBUTION OF LEXICON WORDS")

sw = stopwords.words("french")
sw += ["les", "plus", "cette", "fait", "faire", "être", "deux", "comme", "dont", "tout",
       "ils", "bien", "sans", "peut", "tous", "après", "ainsi", "donc", "cet", "sous",
       "celle", "entre", "encore", "toutes", "pendant", "moins", "dire", "cela", "non",
       "faut", "trois", "aussi", "dit", "avoir", "doit", "contre", "depuis", "autres",
       "van", "het", "autre", "jusqu"]
sw = set(sw)

path = "data/all.txt"
limit = 10**8

with open(path) as f:
    text = f.read()[:limit]
    words = nltk.wordpunct_tokenize(text)
    print(f"{len(words)} words found")
    kept = [w.lower() for w in words if len(w) > 2 and w.isalpha() and w.lower() not in sw and w.lower() in my_lexique]
    voc = set(kept)
    print(f"{len(kept)} words kept ({len(voc)} different word forms)")
    fdist = nltk.FreqDist(kept)
    print(f"Number of appearances of words in our lexicon")
    pprint(fdist.most_common(11))

print("\n--> NAMED-ENTITY RECOGNITION")

textList = ["1969", "1956", "1888", "1892"]
for year in textList:
    print(f"rapport_final/{year}.txt")
    text = open(f"rapport_final/{year}.txt").read()
    print(len(text))
    doc = nlp(text)
    entities = defaultdict(int)
    for ent in doc.ents:
            if ent.label_ == "LOC" and len(ent.text) > 3:
                entities[ent.text] += 1
                sorted_entities = sorted(entities.items(), key=lambda kv: kv[1], reverse=True)

    for res, freq in sorted_entities[:10]:
        print(f"{res} appears {freq} times in the corpus of {year}\n")

print("\n--> LEXICON'S WORDS SIMILARITY")

word1 = "jardin"
pprint(model.wv[word1])

word1_1 = "bois"
#%%
word2 = "végétation"
sim1 = model.wv.similarity(word1, word2)
print(f"{word1} is {100*sim1:.1f}% similar to {word2}\n")

sim1 = model.wv.similarity(word1_1, word2)
print(f"{word1_1} is {100*sim1:.1f}% similar to {word2}\n")

print("-----> Mot bois")
pprint(model.wv.most_similar("bois"))
print("-----> Mot nature")
pprint(model.wv.most_similar("nature"))
print("-----> Mot parc")
pprint(model.wv.most_similar("parc"))
print("-----> Mot jardin")
pprint(model.wv.most_similar("jardin"))
print("-----> Mot arbres")
pprint(model.wv.most_similar("arbres"))


pprint(model.wv.most_similar(positive=['parc', 'bruxelles'], negative=['bois']))
