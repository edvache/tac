"""Named-entity recognition with SpaCy"""

from collections import defaultdict
import sys

import spacy
from spacy.lang.fr.examples import sentences

nlp = spacy.load('fr_core_news_sm')

def test():
    """Basic test on sample sentences"""
    for sent in sentences:
        doc = nlp(sent)
        entities = []
        for ent in doc.ents:
            entities.append(f"{ent.text} ({ent.label_})")
        if entities:
            print(f"'{doc.text}' contains the following entities: {', '.join(entities)}")
        else:
            print(f"'{doc.text}' contains no entities")

def search(arg):
    text = open("module3/1922.txt").read()
    doc = nlp(text)
    entities = defaultdict(int)
    for ent in doc.ents:
        if arg == "PER" or arg == "LOC" or arg == "ORG":
            if ent.label_ == arg and len(ent.text) > 3:
                entities[ent.text] += 1
            sorted_entities = sorted(entities.items(), key=lambda kv: kv[1], reverse=True)

    for res, freq in sorted_entities[:10]:
        print(f"{res} appears {freq} times in the corpus")



if __name__ == "__main__":
    try:
        if sys.argv[1] == "test":
            test()
        elif sys.argv[1] == "search":
            try:
                if sys.argv[2] == "PER" or sys.argv[2] == "LOC" or sys.argv[2] == "ORG":
                    search(sys.argv[2])
            except IndexError:
                print("Unknown option, please use either 'PER' or 'LOC' or 'ORG' or 'ALL'")
        else:
            print("Unknown option, please use either 'test' or 'search'")
    except IndexError:
        print("No option, please specify either 'test' or 'search'")
