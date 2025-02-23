import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 100000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    '''
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    '''
    pages = dict()
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    return pages


def initialize_probabilities(corpus):
    probabilities = {}
    for page in corpus.keys():
        probabilities[page] = 0.0
    return probabilities


def transition_model(corpus, page, damping_factor):
    '''
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    '''
    probabilities = initialize_probabilities(corpus)
    for p in corpus.keys():
        probabilities[p] += (1 - damping_factor) / len(corpus.keys())
    for p in corpus[page]:
        probabilities[p] += damping_factor / len(corpus[page])
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    '''
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    '''
    random_starting_page = random.choice(list(corpus.keys()))
    chain = [random_starting_page]
    current_page = random_starting_page
    for _ in range(SAMPLES):
        transition_probs = transition_model(corpus, current_page, damping_factor)
        next_page = random.choices(
            population=list(transition_probs.keys()),
            weights=list(transition_probs.values()),
            k=1
        )[0]
        chain.append(next_page)
        current_page = next_page
    return calculate_pagerank_without_counter(chain)


def calculate_pagerank_without_counter(output_array):
    # Initialize a dictionary to keep track of counts
    '''
    This function calculates the PageRank values for each page based on
    the frequency of their appearance in the Markov chain output array.
    '''
    page_counts = {}
    for page in output_array:
        if page in page_counts:
            page_counts[page] += 1
        else:
            page_counts[page] = 1
    total_pages = len(output_array)
    pagerank = {page: count / total_pages for page, count in page_counts.items()}
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    '''
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    '''
    PR = {}
    total_page_count = len(corpus)
    for page in corpus:
        PR[page] = 1 / total_page_count
    iterate_count = 0
    while True:
        converge_count = 0
        iterate_count += 1
        new_PR = {}
        for page in corpus:
            random_prob = (1 - damping_factor) / total_page_count
            accumulation = 0
            for i_page in corpus:
                if len(corpus[i_page]) == 0:
                    accumulation += PR[i_page] / total_page_count
                elif page in corpus[i_page]:
                    accumulation += PR[i_page] / len(corpus[i_page])
            linked_prob = damping_factor * accumulation
            new_PR[page] = random_prob + linked_prob
            if abs(new_PR[page] - PR[page]) < 0.001:
                converge_count += 1
        PR = new_PR
        if converge_count == total_page_count:
            return PR


if __name__ == "__main__":
    main()
