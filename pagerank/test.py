from pagerank import *



sample = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
damping_factor = 0.85
n = 10000

answer = sample_pagerank(sample, damping_factor, n)
print(answer)