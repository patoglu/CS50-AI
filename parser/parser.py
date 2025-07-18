import nltk
import sys


nltk.download("punkt_tab")

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
S -> S Conj S
S -> S Conj VP
NP -> N | Det N | Det N PP
VP -> V | V NP | V PP
PP -> P NP
NP -> Adj N
NP -> Det Adj N
NP -> Det N PP 
NP -> NP PP
VP -> Adv V NP
VP -> V PP Adv
VP -> V Adv
VP -> V PP
VP -> VP Conj VP
VP -> V NP PP
NP -> Det AdjList N
AdjList -> Adj
AdjList -> Adj AdjList
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Convert to lowercase
    sentence = sentence.lower()
    tokens = nltk.word_tokenize(sentence)
    word_tokens = [token for token in tokens if any(char.isalpha() for char in token)]
    print(word_tokens)
    return word_tokens

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            has_np_child = False
            for child in subtree.subtrees():
                if child == subtree:
                    continue
                if child.label() == "NP":
                    has_np_child = True
                    break
            if not has_np_child:
                chunks.append(subtree)
    return chunks

if __name__ == "__main__":
    main()
