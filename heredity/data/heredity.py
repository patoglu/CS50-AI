import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    joint_prob = 1.0

    for person in people.keys():
        if people[person]['mother'] is None and people[person]['father'] is None:
            # No parents so calculate unconditional probabilities
            if person in one_gene:
                gene_prob = PROBS["gene"][1]
            elif person in two_genes:
                gene_prob = PROBS["gene"][2]
            else:
                gene_prob = PROBS["gene"][0]

            if person in have_trait:
                trait_prob = PROBS["trait"][1 if person in one_gene else 2 if person in two_genes else 0][True]
            else:
                trait_prob = PROBS["trait"][1 if person in one_gene else 2 if person in two_genes else 0][False]

            joint_prob *= gene_prob * trait_prob

        else:
            # Has parents, calculate based on parents' genes
            father = people[person]["father"]
            mother = people[person]["mother"]

            # Inline function definition for readability
            def parent_prob(parent):
                if parent in two_genes:
                    return 1 - PROBS["mutation"]
                elif parent in one_gene:
                    return 0.5
                else:
                    return PROBS["mutation"]

            mother_prob = parent_prob(mother)
            father_prob = parent_prob(father)

            if person in one_gene:
                gene_prob = (mother_prob * (1 - father_prob)) + ((1 - mother_prob) * father_prob)
            elif person in two_genes:
                gene_prob = mother_prob * father_prob
            else:
                gene_prob = (1 - mother_prob) * (1 - father_prob)
            if person in have_trait:
                trait_prob = PROBS["trait"][1 if person in one_gene else 2 if person in two_genes else 0][True]
            else:
                trait_prob = PROBS["trait"][1 if person in one_gene else 2 if person in two_genes else 0][False]

            joint_prob *= gene_prob * trait_prob

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `one_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in two_genes:
            gene_count = 2
        elif person in one_gene:
            gene_count = 1
        else:
            gene_count = 0

        if person in have_trait:
            trait_status = True
        else:
            trait_status = False

        probabilities[person]["gene"][gene_count] += p
        probabilities[person]["trait"][trait_status] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        gene_total = sum(probabilities[person]["gene"].values())
        for key in probabilities[person]["gene"]:
            probabilities[person]["gene"][key] /= gene_total

        trait_total = sum(probabilities[person]["trait"].values())
        for key in probabilities[person]["trait"]:
            probabilities[person]["trait"][key] /= trait_total


if __name__ == "__main__":
    main()
