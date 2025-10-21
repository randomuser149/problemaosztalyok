def parse_rules(filename):
    with open(filename) as file:
        grammar = {}
        nonterminals = set()
        for line in file:
            if "->" not in line:
                continue
            left_hand_side, right_hand_side = line.strip().split("->",1)
            left_hand_side = left_hand_side.strip()
            nonterminals.add(left_hand_side)
            for rule in [item.strip() for item in right_hand_side.split("|")]:
                grammar.setdefault(left_hand_side, []).append(rule)
    return dict(grammar), nonterminals

parse_rules("input.txt")