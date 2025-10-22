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
        #print(f" nonterminals: {nonterminals}")
        #print(f" nonterminal lengths, no repeats, in reversed order: {nonterminal_length}")
        index = 0
        token_list = [] # stores found tokens in a list
        while index < len(input_string):
            matched = False # track whether a nonterminal was matched at this index
            for length in nonterminal_length: # checks every length starting from given index
                #print(f" current length: {length}")
                if index + length <= len(input_string): # checks against out of bounds
                    substring = input_string[index:index+length]
                    #print(f" if loop current: {input_string[index:index+length]}")
                    if substring in nonterminals: # if the current substring is found in nonterminals 
                        token_list.append(substring) # append the substring to the token_list
                        #print(f" found match, adding: {substring}")
                        index = index+length # correct the index to skip the length of found substring
                        matched = True # the if not matched doesn't run
                        break
            if not matched: # if no match found
                #print(f" did not find match, adding: {input_string[index]}")
                token_list.append(input_string[index]) # append only the char to the token_list
                index += 1 # increase index by 1
        return token_list
    return splitter

def compute_productive_nonterminals(grammar, splitter):
    productive_nonterminals = set() # (set) stores productive nonterminals
    matched = True # tracks whether a productive nonterminal was found in that iteration, set to True ensures the while runs at least once
    while matched: # keep looping until no new productive nonterminals are discovered
        matched = False
        for nonterminal, expansions in grammar.items(): # unpacking each rule into nonterminal and its expansions (list), iterate over each nonterminal
            #print(f"\n nonterminal is {nonterminal} | expansions are {expansions}")
            if nonterminal in productive_nonterminals: # if already found, skip to next iteration
                #print(f" nonterminal already in productive set {nonterminal}")
                continue
            for expansion in expansions: # for each expansion to given nonterminal
                #print(f" current expansion is: {expansion} | full expansion list for nonterminal is {expansions}")
                if all((token.islower() or (token in productive_nonterminals)) for token in splitter(expansion)): # if all tokens are lowercase (terminal) or are known productive nonterminals
                    #[print(f"\t token is productive: {token}") for token in splitter(expansion)]
                    #print(f" all tokens in expansion are productive {splitter(expansion)}\n appending {nonterminal} to set")
                    productive_nonterminals.add(nonterminal) # add to the set
                    matched = True # ensures the loop runs once more
                    break # exits if one productive expansion is found
                #else:
                #    for token in splitter(expansion):
                #        print(f"\t token is productive: {token}") if (token.islower() or token in productive_nonterminals) else print(f"\t token is not productive: {token}")
    return productive_nonterminals

def compute_reachable_nonterminals(grammar, splitter, start_symbol):
    reachable_nonterminals_set = set() # (set) stores reachable nonterminals
    stack = [start_symbol] if start_symbol in grammar else [] # (stack) stores to be checked items, starts with start_symbol if it has a rule - [LIFO]
    print(f" starting stack is: {stack}")
    while stack: # until stack is empty
        print(f"\n current reachable set is: {reachable_nonterminals_set}")
        print(f" current stack to explore: {stack}")
        current = stack.pop() # remove last added item, store it in current for computing.
        print(f" current item: {current}")
        if current in reachable_nonterminals_set: # if current nonterminal is already marked, skip
            print(f"\t current already in set, skipping: {current}")
            continue
        print(f"\t current not in set, adding: {current}")
        reachable_nonterminals_set.add(current) # mark current nonterminal as reachable (adding it to the set)
        print(f" trying for expansion(s) of {current}")
        if current in grammar.keys(): # if nonterminal has a rule (is in the left hand side)
            print(f"\t expansion(s) for current item: {grammar.get(current)}")
            for expansion in grammar.get(current): # iterate over each value for a given key
                print(f" current expansion is: {expansion}")
                for token in splitter(expansion): # iterate over each token for a given expansion
                    print(f"\t current token is {token} | tokenized from {expansion}")
                    if token in grammar.keys() and token not in reachable_nonterminals_set: # if token has a rule and is not marked yet, mark it
                        print(f"\t\t marking token as reachable: {token}")
                        stack.append(token)
                    else: # print for debugging purposes
                        print(f"\t\t skipping token, has no rule(s): {token}") if token not in grammar.keys() else print(f"\t\t skipping token, already marked: {token}")

    return reachable_nonterminals_set

grammar, nonterminals = parse_rules("input.txt")
splitter = make_splitter(nonterminals)
print(f" output tokens: {splitter("SDFGxDHVX")}")
print(f" productive set: {compute_productive_nonterminals(grammar,splitter)}")
print(f" reachable set: {compute_reachable_nonterminals(grammar,splitter,"S")}")