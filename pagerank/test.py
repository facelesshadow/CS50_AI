from pagerank import *



corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
damping_factor = 0.85
n = 10000

i_dict = corpus.copy()
for element in corpus:
    i_dict[element] = []
    for element2 in corpus:
        if element in corpus[element2]:
            i_dict[element].append(element2)

        if not corpus[element2]:
            i_dict[element].append(element2)


print(i_dict)