import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # Dictionary in which keys - Pages and value - Set of pages to which that page links to.
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Corpus = Dictionary . Page - String on which we are currently . damping_factor - float
    # return a dict with all pages and their corresponding probability
    p_corpus = corpus.copy()
    total_pages = len(corpus)
    total_i = len(corpus[page])
    i_list = list(corpus[page])

    for element in p_corpus:
        if not i_list:
            p_corpus[element] = (1 / total_pages)
        else:
            p_corpus[element] = (1 - damping_factor)/total_pages

            if element in i_list:
                p_corpus[element] += (damping_factor/total_i)
    # Add (1-d)/ length probability to all the pages probab
    # add d/n(i) probability to all pages probab...9

    # with damping_factor, choose
    return p_corpus
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    '''
    run a loop n times,
    and for the first iteration, choose a random page from corpus.
    put that page into the transition model, then get the new transition model
    put those probabilities, and choose a new page depending on the probabilities,,
    if page x, then add 1 to the new dictionary of samples
    keep doing it and then divide all of it by n at the end of the loop....
    return the new sample dict to the mf....
    '''
    sample_corpus = corpus.copy()
    for element in sample_corpus:
        sample_corpus[element] = 0

    first_random = random.choice(list(corpus.keys()))
    sample_corpus[first_random] = 1
    sample_state = transition_model(corpus, first_random, damping_factor)

    for i in range(n-1):
        '''
        chosen_webpage = random.choices(
        list(webpage_probabilities.keys()),
        weights=list(webpage_probabilities.values()),
        k=1
        )[0]

        '''
        choosen_page = random.choices(
            list(sample_state.keys()),
            weights=list(sample_state.values()),
            k=1
        )[0]

        sample_corpus[choosen_page] += 1
        sample_state = transition_model(corpus, choosen_page, damping_factor)

    for element in sample_corpus:
        sample_corpus[element] = sample_corpus[element] / n

    return sample_corpus
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}
    threshold = 0.0005
    N = len(corpus)

    for key in corpus:
        ranks[key] = 1 / N


    while True:
        count = 0
        for key in corpus:
            new = (1 - damping_factor) / N
            sigma = 0
            for page in corpus:
                if key in corpus[page]:
                    num_links = len(corpus[page])
                    sigma = sigma + ranks[page] / num_links
                elif not corpus[page]:
                    num_links = len(corpus)
                    sigma = sigma + ranks[page] / num_links
            sigma = damping_factor * sigma
            new += sigma
            if abs(ranks[key] - new) < threshold:
                count += 1
            ranks[key] = new
        if count == N:
            break
    return ranks


    raise NotImplementedError


if __name__ == "__main__":
    main()
