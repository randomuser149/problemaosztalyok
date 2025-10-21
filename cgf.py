def parse_rules(filename):
    """
    Parse a grammar file of the form 'LHS -> RHS1 | RHS2 | ...'.
    Returns:
        grammar: dict mapping each expression (LHS) to a list of expansions (RHS)
        nonterminals: set of all nonterminal symbols (from LHS, since if one appears only in the RHS, it is unreferenced, having no use)
    """
    with open(filename) as file:
        grammar = {} # (dict) defines each expression (key) and its expansions (values)
        nonterminals = set()
        for line in file:
            if "->" not in line: # if line has no rule symbol, skip
                continue
            left_hand_side, right_hand_side = line.strip().split("->",1) # split into expressions (str) and their expansions (list)
            left_hand_side = left_hand_side.strip()
            nonterminals.add(left_hand_side) # collect nonterminals from the left hand side
            for rule in [item.strip() for item in right_hand_side.split("|")]: # for each option to given lhs
                grammar.setdefault(left_hand_side, []).append(rule) # append values to or create the new key + values
    return dict(grammar), nonterminals

parse_rules("input.txt")