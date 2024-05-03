import requests
import re


def fetch_names(limit: int = 100, region: str = "Q183") -> list:
    url = "https://query.wikidata.org/sparql"
    query = f"""
    SELECT DISTINCT ?person ?personLabel WHERE {{
      ?person wdt:P31 wd:Q5;  # Q5 stands for human
        (wdt:P27|wdt:P19|wdt:P551) wd:{region}.  # P27 for citizenship, P19 for place of birth, P551 for place of residence, Q183 for Germany
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de". }}
    }}
    LIMIT {limit}
    """
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
    response = requests.get(url, headers=headers, params={'query': query, 'format': 'json'})
    data = response.json()
    return [result['personLabel']['value'] for result in data['results']['bindings']]

def name_pattern(string) -> bool:
    """
    rough filter, some names contain 2 letters.
    TODO: doesn't cover uppercase with accent
    """
    finds = re.findall(pattern=r"[A-Z]{2,}|\W|\d", string=string, flags=re.UNICODE) 
    return len(finds) == 0

def clean(names: List[str]) -> List[str]:
    # unfold "Hans-Peter" -> ["Hans", "Peter"]
    names_unfolded = []
    for name in names:
        if "-" in name:
            names_unfolded.extend(name.split("-"))
        else:
            names_unfolded.append(name)
    return [f for f in names_unfolded if (name_pattern(f)) and (len(f) > 2)]


"""
Q183: germany
Q36: polish
Q41: greek
Q43: turkish
"""
region = "Q36"
names = fetch_names(limit=2_000, region=region)  # fetch 2_000 names
"""
names_new = fetch_names(limit=50, region=region)
names.extend(names_new)
names = list(set(names))
print(len(names))
"""
names_valid = [n for n in names if len(n.split()) == 2]  # for simplification. problem: Sabine von Eltz etc
names_valid = list(set(names_valid))  # uniuqes

first_names = clean([n.split()[0] for n in names_valid])
last_names = clean([n.split()[1] for n in names_valid])

with open(f"last_names_{region}.txt", "w", encoding="utf8") as f:
    f.write("\n".join(last_names))
with open(f"first_names_{region}.txt", "w", encoding="utf8") as f:
    f.write("\n".join(first_names))
