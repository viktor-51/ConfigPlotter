import regex as re

def make_into_pattern(string, escape):
    if escape: string = re.escape(string)

    new_string = string.replace("\\*", "(.)*")

    pattern = re.compile(new_string)

    return pattern

def find_all_matches(string, search_fields, escape, full_match = True):
    return find_n_matches(string, search_fields, escape, find_all = True, full_match = full_match)

def search(string, search_fields, escape, full_match = True):
    match = find_n_matches(string, search_fields, escape, n = 1, full_match = full_match)

    if match:
        return match[0]
    else:
        return None

def span(string, search_field):
    escape = False

    pattern = make_into_pattern(string, escape)
    match = pattern.search(search_field)

    return match.span()

def find_n_matches(string, search_fields, escape, n = 1, find_all = False, full_match = True):
    pattern = make_into_pattern(string, escape)
    matches = []
    
    if find_all:
        n = -1

    for field in search_fields:
        if type(field) is str:
            if full_match:
                match = pattern.fullmatch(field)
            else:
                match = pattern.search(field)
            
            if match:
                n -= 1
                matches.append(field)

                if n == 0:
                    return matches

    if find_all and len(matches) > 0:
        return matches
    else:
        return None


