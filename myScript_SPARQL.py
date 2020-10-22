"""Query Wikidata for Belgian politicians"""

import argparse
import json
import sys

from datetime import datetime as dt

from SPARQLWrapper import SPARQLWrapper, JSON

def get_rows(gender):
    """Retrieve results from SPARQL"""
    endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
    sparql = SPARQLWrapper(endpoint)

    try:
        if gender == "M" or gender == "Male":
            statement = """
            SELECT DISTINCT ?person ?personLabel ?dateBirth ?dateDeath WHERE {
                ?person wdt:P27 wd:Q31 .
                ?person wdt:P106 wd:Q82955 .
                ?person wdt:P21 wd:Q6581097 .
                ?person wdt:P569 ?dateBirth .
                OPTIONAL {?person wdt:P570 ?dateDeath .}
                SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
                }
            ORDER BY ?personLabel
            """
        elif gender == "F" or gender == "Female":
            statement = """
            SELECT DISTINCT ?person ?personLabel ?dateBirth ?dateDeath WHERE {
                ?person wdt:P27 wd:Q31 .
                ?person wdt:P106 wd:Q82955 .
                ?person wdt:P21 wd:Q6581072 .
                ?person wdt:P569 ?dateBirth .
                OPTIONAL {?person wdt:P570 ?dateDeath .}
                SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
                }
            ORDER BY ?personLabel
            """
    except KeyError:
        print("Unknown gender, try 'F'/'M' or 'Female'/'Male'")

    sparql.setQuery(statement)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    rows = results['results']['bindings']
    if gender == "M" or gender == "Male":
        print(f"\n{len(rows)} Male Belgian politicians found\n")
    if gender == "F" or gender == "Female":
        print(f"\n{len(rows)} Female Belgian politicians found\n")
    return rows

def show(rows, n):
    """Display n politicians (default=10)"""
    date_format = "%Y-%m-%dT%H:%M:%SZ"

    print(f"Displaying the first {n}:\n")
    for row in rows[:int(n)]:
        print(f"Name: {row['personLabel']['value']}")

if __name__ == "__main__":
    try:
        service = sys.argv[1]
        my_rows = get_rows(sys.argv[1])
        number = sys.argv[2] if sys.argv[2] else 10
        show(my_rows, number)
    except KeyError:
        print("Unknown gender, try 'F'/'M' or 'Female'/'Male'")
