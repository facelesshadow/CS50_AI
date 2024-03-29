from pagerank2 import *



corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
damping_factor = 0.85

answer = iterate_pagerank(corpus, damping_factor)

print(answer)