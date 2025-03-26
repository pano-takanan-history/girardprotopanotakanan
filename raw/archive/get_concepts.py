import csv
from collections import defaultdict
from lingpy import Wordlist
from pysem import to_concepticon


wl = Wordlist("ppt.tsv")

concepts = [[
    "GLOSS",
    "CONCEPTICON_ID",
    "CONCEPTICON_GLOSS",
    "PROTO_ID"
    ]]

checkup = defaultdict()
for i in wl:
    ID = wl[i, "proto_set"]
    print(wl[i])
    p_concept = wl[i, "proto_concept"].replace('**', '').replace('*', '')
    concept_source = wl[i, "concept"]

    mapped = to_concepticon([{"gloss": p_concept}], language="en")

    if p_concept not in checkup:
        if mapped[p_concept]:
            cid, cgl = mapped[p_concept][0][:2]
        else:
            cid, cgl = "", ""

        checkup[p_concept] = [cid, cgl]
        concepts.append([
            p_concept, cid, cgl, ID
        ])

with open("../etc/concepts.tsv", "w", encoding="utf8") as file:
    writer = csv.writer(file, delimiter="\t")
    writer.writerows(concepts)
