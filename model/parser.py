import nltk

from typing import Set, List
from collections import defaultdict


def parse(grammar: nltk.grammar.CFG, sentence: List[str]) -> Set[nltk.ImmutableTree]:
    """
    Check whether a sentence in the language of grammar or not. If it is, parse it.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of sentence.
        sentence: Input sentence that will be tested.

    Returns:
        tree_set: Set of generated parse trees.
    """
    # YOUR CODE HERE
    #     TODO:
    #         1) Extend your CKY recognizer into a parser by adding backpointers. You
    #         should extract the set of all parse trees from the backpointers in the chart.
    #         2) Note that only 'ImmutableTree` can be used as elements of Python sets.
    ############################# STUDENT SOLUTION ##################################
    
    print("Starting...")
    
    Set[nltk.ImmutableTree]
    n = len(sentence)

    table = [[[] for j in range(n)] for i in range(n)]

    # Create a defaultdict to store grammar productions by their right-hand sides
    production_dict = defaultdict(list)
    for production in grammar.productions():
        production_dict[production.rhs()].append(production)

    # Fill in the chart with lexical entries
    for j in range(n):
        # For each word in the sentence, add non-terminals based on grammar productions
        for production in grammar.productions(rhs=sentence[j]):
            table[j][j].append(nltk.Tree(production.lhs(), [production.rhs()]))

    print("Filling the table...")

    # Fill in the table using non-terminal productions
    for length in range(2, n+1):
        for i in range(n - length + 1):
            trees = []
            j = i + length - 1
            for k in range(i, j):
                right = table[i][k]
                down = table[k+1][j]
                for r_tree in right:
                    for d_tree in down:
                        key = (r_tree.label(), d_tree.label())

                        if production_dict.__contains__(key):
                            for productions in production_dict[key]:
                                trees.append(nltk.Tree(production.lhs(), [r_tree, d_tree]))

            table[i][j] = trees
    
    trees_found = []

    print("Finding trees...")

    for tree in table[0][n-1]:
        if str(tree.label()) == str(grammar.start()):
            trees_found.append(tree)

    return set(trees_found)
    #################################################################################

def count(grammar: nltk.grammar.CFG, sentence: List[str]) -> int:
    """
    Compute the number of parse trees without actually computing the parse tree.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of sentence.
        sentence: Input sentence that will be tested.

    Returns:
        tree_count: Number of generated parse trees.
    """
    ############################# STUDENT SOLUTION ##################################
    n = len(sentence)

    # Initialize the CYK table with sets
    table = [[set([]) for j in range(n)] for i in range(n)]

    # Create a defaultdict to store grammar productions by their right-hand sides
    production_dict = defaultdict(list)
    for production in grammar.productions():
        production_dict[production.rhs()].append(production)

    # Fill in the table with terminal productions
    for j in range(n):
        for production in grammar.productions(rhs=sentence[j]):
            table[j][j].add(production.lhs())

    # Fill in the table using non-terminal productions
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for r_lhs in table[i][k]:
                    for d_lhs in table[k + 1][j]:
                        key = (r_lhs, d_lhs)
                        if key in production_dict:
                            for production in production_dict[key]:
                                table[i][j].add(production.lhs())

    # Count the number of distinct parses
    return len(table[0][n - 1])
    #################################################################################