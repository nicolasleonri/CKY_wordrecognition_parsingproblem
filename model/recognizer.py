import nltk
from utils import print_chart
from typing import List

from collections import defaultdict
from nltk.tokenize import wordpunct_tokenize


def recognize(grammar: nltk.grammar.CFG, sentence: List[str]) -> bool:
    """
    Recognize whether a sentence in the language of grammar or not.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of sentence.
        sentence: Input sentence that will be tested.

    Returns:
        truth_value: A bool value to determine whether if the sentence
        is in the grammar provided or not.
    """
    ############################ STUDENT SOLUTION ###########################
    # Get the length of the input sentence
    n = len(sentence)

    # Initialize the CYK table with sets
    table = [[set([]) for j in range(n)] for i in range(n)]

    # Create a defaultdict to store grammar productions by their right-hand sides
    production_dict = defaultdict(list)
    for production in grammar.productions():
        production_dict[production.rhs()].append(production)

    # Fill in the table with terminal productions
    for j in range(0, n):
        # For each production matching the current word in the sentence
        for production in grammar.productions(rhs=sentence[j]):
            # Add the left-hand side of the production to the cell
            table[j][j].add(production.lhs())

    # Fill in the table using non-terminal productions
    for length in range(2, n+1):  
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                right = table[i][k]
                down = table[k+1][j]
                # Iterate over combinations of non-terminals from the two halves
                for r_lhs in right:
                    for d_lhs in down:
                        key = (r_lhs, d_lhs)
                        # If the combination exists in the grammar, add resulting non-terminals
                        if production_dict.__contains__(key):
                            for productions in production_dict[key]:
                                table[i][j].add(productions.lhs())
                        
    # Check if the top-right cell is empty, indicating grammaticality    
    return len(table[0][n-1]) != 0
    #########################################################################