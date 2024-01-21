import argparse
import nltk

from nltk.tree import Tree
from model.recognizer import recognize
from model.parser import parse, count

GRAMMAR_PATH = './data/atis-grammar-cnf.cfg'


def main():
    parser = argparse.ArgumentParser(
        description='CKY algorithm'
    )

    parser.add_argument(
        '--structural', dest='structural',
        help='Derive sentence with structural ambiguity',
        action='store_true'
    )

    parser.add_argument(
        '--recognizer', dest='recognizer',
        help='Execute CKY for word recognition',
        action='store_true'
    )

    parser.add_argument(
        '--parser', dest='parser',
        help='Execute CKY for parsing',
        action='store_true'
    )

    parser.add_argument(
        '--count', dest='count',
        help='Compute number of parse trees from chart without \
              actually computing the trees (Extra Credit)',
        action='store_true'
    )

    args = parser.parse_args()

    # load the grammar
    grammar = nltk.data.load(GRAMMAR_PATH)
    # load the raw sentences
    s = nltk.data.load("grammars/large_grammars/atis_sentences.txt", "auto")
    # extract the test sentences
    t = nltk.parse.util.extract_test_sentences(s)

    if args.structural:

        # Sentence A with structural ambiguity: "I saw someone with a telescope."
        # Example from: https://ecampusontario.pressbooks.pub/essentialsoflinguistics2/chapter/a1-3-structural-ambiguity/
        sentence_A_1 = "(S (NP (N (I))) (VP (V (saw)) (NP (N (someone))) (PP (P (with)) (NP (Det (a)) (N (telescope.))))))"
        sentencea_A_2 = "(S (NP (N (I))) (VP (V (saw)) (NP (N (someone)) (PP (P (with)) (NP (Det (a)) (N (telescope.))))) ) ) "

        # Generating trees
        tree1 = Tree.fromstring(sentence_A_1)
        tree2 = Tree.fromstring(sentencea_A_2)

        print("Structure 1 of sentence A:")
        tree1.pretty_print(unicodelines=True, nodedist=3) #Interpretation: "I was using a telescope, and I saw someone." (PP modifies VP) 
        print("Structure 2 of sentence A:")
        tree2.pretty_print(unicodelines=True, nodedist=3) # Interpration: "I saw someone, and that person had a telescope." (PP modifies NP)

        # Sentence B with structural ambiguity: "Sam wears a bright yellow shirt."
        # Example from: http://www.sfu.ca/~hedberg/2013_1_Syntactic_ambiguity_trees.pdf 
        sentence_B_1 = "(S (NP (Sam)) (VP (V (wears)) (NP (Det (a)) (N (AdjP (Adv (bright)) (Adj (yellow))  ) (N (shirt.)) ))) )"
        sentence_B_2 = "(S (NP (Sam)) (VP (V (wears)) (NP (Det (a)) (NP (Adv (bright)) (Adj (yellow)) (N (shirt.))))))"

        # Generating trees
        tree3 = Tree.fromstring(sentence_B_1) 
        tree4 = Tree.fromstring(sentence_B_2) 

        print("Structure 1 of sentence B:")
        tree3.pretty_print(unicodelines=True, nodedist=3) #Interpretation: "The shirt has a bright yellow color." (Only one noun phrase)
        print("Structure 2 of sentence B:")
        tree4.pretty_print(unicodelines=True, nodedist=3) #Interpretation: "The shirt is bright and the shirt is also yellow."" (Two noun phrases)


    elif args.recognizer:
        grammatical = [
        ["need", "a", "flight", "right", "now"],
        ["need", "a", "flight", "right", "tomorrow"], # false positive
        ["book", "please", "a", "flight", "to", "miami",],
        ["list", "flights", "today",],
        ['my', "friend", 'goes', 'somewhere', 'tomorrow'], # describes someone's plan to go somewhere the next day
        ['please', 'stop', 'for', 'tonight'],
        ['stop', 'for', 'tonight', 'please'], # alternative phrasing
        ['my', 'mother', 'flies', 'to', 'minnesota', 'on', 'tuesday'],
        ['get', 'me', 'the', 'cheapest', 'flight', 'from', 'london', 'to', 'washington'], # a request
        ['which', 'flight', 'is', 'leaving', 'by', 'nine'],
        ['which', 'flight', 'is', 'leaving', 'on', 'the', 'morning'],
        ['get', 'me', 'a', 'plane', "preferably", "at", 'noon'],
        ['get', 'me', 'a', 'train', "preferably", "at", 'noon'] # alternative transportation
        ]

        ungrammatical = [
        ["book", "please", "two", "tickets", "to", "miami",],
        ["book", "please", "a", "flight", "to", "miami", 'from', 'berlin'],
        ["a", "flight", 'from', 'berlin', 'to', 'london'],
        ['my', 'mother', 'flew', 'to', 'minnesota', 'last', 'tuesday'], # "flew" instead of "flies"
        ['get', 'me', 'the', 'quickest', 'flight', 'from', 'london', 'to', 'washington'], # superlative "quickest" instead of "cheapest"
        ['where', 'is', 'the', 'airport'], # asking about the location of the airport
        ['have', 'a', 'nice', 'flight'],
        ['stop', 'please', 'for', 'tonight',],
        ['where', 'does', 'it', 'stop'],
        ['how', 'long', 'do', 'you', 'need']
        ]
        
        for sents in grammatical:
            val = recognize(grammar, sents)
            if val:
                print("'{}' is in the language of CFG.".format(sents))
            else:
                print("'{}' is not in the language of CFG.".format(sents))

        for sents in ungrammatical:
            val = recognize(grammar, sents)
            if val:
                print("'{}' is in the language of CFG.".format(sents))
            else:
                print("'{}' is not in the language of CFG.".format(sents))

    elif args.parser:
        # We test the parser by using ATIS test sentences.
        print("ID\t Predicted_Tree\tLabeled_Tree")
        for idx, sents in enumerate(t):
            tree = parse(grammar, sents[0])
            print("{}\t {}\t \t{}".format(idx, len(tree), sents[1]))

        # YOUR CODE HERE
        #     TODO:
        #         1) Choose an ATIS test sentence with a number of parses p
        #         such that 1 < p < 5. Visualize its parses. You can use `draw` 
        #         method to do this.
            
        # Choose an ATIS test sentence dynamically with a number of parses p such that 1 < p < 5.
        for idx, sents in enumerate(t):
            num_parses = len(parse(grammar, sents[0]))
            if 1 < num_parses < 5:
                sentence_to_visualize = sents[0]
                predicted_trees = parse(grammar, sentence_to_visualize)

            # Visualize parse trees using the `draw` method
                print(f"Visualizing parses for sentence at index {idx}: {sentence_to_visualize}")
                for i, tree in enumerate(predicted_trees):
                    tree.draw()
                break  # Stop after finding the first suitable sentence
       

    elif args.count:
        print("ID\t Predicted_Tree\tLabeled_Tree")
        for idx, sents in enumerate(t):
            num_tree = count(grammar, sents[0])
            print("{}\t {}\t \t{}".format(idx, num_tree, sents[1]))


if __name__ == "__main__":
    main()
