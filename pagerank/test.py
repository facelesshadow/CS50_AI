from pagerank import *



sample = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
damping_factor = 0.85
page = "1.html"

answer = transition_model(sample, page, damping_factor)
print(answer)