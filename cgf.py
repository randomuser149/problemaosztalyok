with open("input.txt","r") as file:
    grammar = {}
    nonterminals = set()
    for line in file:
        left_hand_side, right_hand_side = line.strip().split("->",1)
        left_hand_side = left_hand_side.strip()
        right_hand_side = [item.strip() for item in right_hand_side.split("|")]
        nonterminals.add(line[0].strip())
        for rule in right_hand_side:
            grammar[line[0].strip()]=rule.strip() # overwrites prev definitons, need fix to update if key is present
            