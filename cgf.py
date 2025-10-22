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

def make_splitter(nonterminals):
    nonterminal_length = sorted({len(i) for i in nonterminals}, reverse=True) # collects nonterminal lenghts, no repeats, in reversed order 
    def splitter(input_string):
        print(f" nonterminals: {nonterminals}")
        print(f" nonterminal lengths, no repeats, in reversed order: {nonterminal_length}")
        index = 0
        token_list = [] # stores found tokens in a list
        while index < len(input_string):
            matched = False # track whether a nonterminal was matched at this index
            for length in nonterminal_length: # checks every length starting from given index
                print(f" current length: {length}")
                if index + length <= len(input_string): # checks against out of bounds
                    substring = input_string[index:index+length]
                    print(f" if loop current: {input_string[index:index+length]}")
                    if substring in nonterminals: # if the current substring is found in nonterminals 
                        token_list.append(substring) # append the substring to the token_list
                        print(f" found match, adding: {substring}")
                        index = index+length # correct the index to skip the length of found substring
                        matched = True # the if not matched doesn't run
                        break
            if not matched: # if no match found
                print(f" did not find match, adding: {input_string[index]}")
                token_list.append(input_string[index]) # append only the char to the token_list
                index += 1 # increase index by 1
        return token_list
    return splitter


grammar, nonterminals = parse_rules("input.txt")
splitter = make_splitter(nonterminals)
print(f" output tokens: {splitter("SDFGxDHVX")}")