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
                if rule == "": # skip if line has rule, but rule is empty.
                    continue
                grammar.setdefault(left_hand_side, []).append(rule) # append values to or create the new key + values
    return dict(grammar), nonterminals

def expand_and_merge(symbols, grammar, productive_nonterminals):
    print(f"NEW CALL with symbols: {symbols}")
    results = []
    print(f" current working symbols list is: {symbols}")
    if all((symbol in productive_nonterminals) for symbol in symbols): print(f"symbols already marked as productive, skipping {symbols}")
    # if all are terminals or productive nonterminals
    if all(symbol.islower() or symbol in productive_nonterminals for symbol in symbols):
        results.append(symbols)
        print(f" all symbols are either terminals or marked productive - adding symbols {symbols}")

    for index, symbol in enumerate(symbols): # unpacking symbols into separate chars (symbol) and their indexes, iterate over each pair
        print(f" current index: {index} current symbol {symbol}")
        if symbol in grammar.keys(): # if given symbol is in left hand side of dictionary (so is expandable)
            print(f" \tsymbol is in grammar lhs: {symbol}")
            print(f" \texpansions of current symbol {symbol} are: {grammar[symbol]}")
            for expansion in grammar[symbol]: # for each value (expansion) to a given key
                print(f" \t\tcurrent expansions is {expansion}")
                # "switch out" the symbol while keeping the order of the list and breaking up the extension string into characters
                new_symbols = symbols[:index] + list(expansion) + symbols[index+1:]
                print(f" \t\t\tnew string is {new_symbols}")
                print(f" \t\t\tmade out of {symbols[:index]} + {list(expansion)} + {symbols[index+1:]}")
                # calls itself again to check whether the list with the new symbols can be "switched out" even more
                results.extend(expand_and_merge(new_symbols, grammar, productive_nonterminals)) # use list.extend to avoid nested lists 
                print(f"\nEND OF CALL with symbols {symbols}\n")
        else:
            print(f" \tsymbol is NOT in grammar lhs, skipping: {symbol}")
    print(f" returned result list of 'splitter': {results}\n")

    max_merge_size = 10  # expansions can be up to 10 characters

    for size in range(2, min(len(symbols),max_merge_size) + 1):  # try pairs, triplets, ... up to 10, stop if theres not that many characters
        print(f" current symbols are: {symbols}")
        print(f" trying merge size: {size}")
        for index in range(len(symbols)): # check every possible starting index
            if index + size <= len(symbols): # only continue if substring size isn't out of bounds
                print(f" \tcurrent index of size {size}: {index}")
                merged = "".join(symbols[index:index+size]) # save the current substring
                print(f" \t\tmerged string: {merged}")
                if merged in grammar: # if substring is in grammar (has a rule)
                    print(f" \t\tfound merged string in grammar: {merged}")
                    # "switch out" the characters with a valid symbol made out of those characters
                    new_symbols = symbols[:index] + [merged] + symbols[index+size:]
                    print(f" \t\t\tnew symbols are {new_symbols}")
                    # calls itself again to check whether the list with the new symbols can be processed (merged) even more
                    results.extend(expand_and_merge(new_symbols, grammar, productive_nonterminals))
                print(f" \t\tmerged string NOT found in grammar {merged}\n")
    return results

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
                """NEEDS DEBUG PRINTS"""
                symbols = expand_and_merge(list(expansion), grammar, productive_nonterminals) # take current expansion, split into symbols, and explore what new substrings/merges it can produce
                for symbol in symbols:  # for each symbol sublist of symbols
                    if all(token.islower() or token in productive for token in symbol): # if all tokens (items) of sublist are lowercase or productive nonterminals only
                        productive_nonterminals.add(nonterminal) # add to the set
                        matched = True # ensures the loop runs once more
                        break # exits if one productive expansion is found
    return productive_nonterminals

def compute_reachable_nonterminals(grammar, splitter, start_symbol):
    reachable_nonterminals_set = set() # (set) stores reachable nonterminals
    stack = [start_symbol] if start_symbol in grammar else [] # (stack) stores to be checked items, starts with start_symbol if it has a rule - [LIFO]
    #print(f" starting stack is: {stack}")
    while stack: # until stack is empty
        #print(f"\n current reachable set is: {reachable_nonterminals_set}")
        #print(f" current stack to explore: {stack}")
        current = stack.pop() # remove last added item, store it in current for computing.
        #print(f" current item: {current}")
        if current in reachable_nonterminals_set: # if current nonterminal is already marked, skip
            #print(f"\t current already in set, skipping: {current}")
            continue
        #print(f"\t current not in set, adding: {current}")
        reachable_nonterminals_set.add(current) # mark current nonterminal as reachable (adding it to the set)
        #print(f" trying for expansion(s) of {current}")
        if current in grammar.keys(): # if nonterminal has a rule (is in the left hand side)
            #print(f"\t expansion(s) for current item: {grammar.get(current)}")
            for expansion in grammar.get(current): # iterate over each value for a given key
                """THE PART BELOW IS BROKEN NEEDS FIXING"""
                """
                #print(f" current expansion is: {expansion}")
                for token in splitter(expansion): # iterate over each token for a given expansion
                    #print(f"\t current token is {token} | tokenized from {expansion}")
                    if token in grammar.keys() and token not in reachable_nonterminals_set: # if token has a rule and is not marked yet, mark it
                        #print(f"\t\t marking token as reachable: {token}")
                        stack.append(token)
                    #else: # print for debugging purposes
                        #print(f"\t\t skipping token, has no rule(s): {token}") if token not in grammar.keys() else print(f"\t\t skipping token, already marked: {token}")
                        """
    return reachable_nonterminals_set

grammar, nonterminals = parse_rules("input.txt")

"""
#print(f" productive set: {compute_productive_nonterminals(grammar,splitter)}")
#print(f" reachable set: {compute_reachable_nonterminals(grammar,splitter,"S")}")

# take the intersection of productive and reachable nonterminals. if empty, then no paths to terminal strings exist.
result = compute_productive_nonterminals(grammar,splitter) & compute_reachable_nonterminals(grammar,splitter,"S")
"""
print("YES" if result else "NO")