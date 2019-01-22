import os
import sys
import re
import itertools
import glob

"""Raw and badly-working pre-processing script to build patterns from multiple verbal roots and then to insert necessary vowels.
Obtained patterns are fed to grep."""


def read_patterns(pattern_file):
    root_types = []
    patterns = []
    with open(pattern_file) as file:
        for line in file:
            root_type, pattern = line.split(None, 2) ## breaks if a file has an empty line
            root_types.append(root_type)
            patterns.append(pattern)

    return dict(zip(root_types, patterns))


def read_roots_and_stems(roots_file):
    roots_and_stems = []
    with open(roots_file) as file:
        triples = itertools.zip_longest(*[iter(file)] * 3, fillvalue='') 
        for triple in triples:
            if triple[0].strip("\n").isalpha():
                root_stem_value = (triple[0].strip("\n"), triple[1].strip(":\n"))
                roots_and_stems.append(root_stem_value)
    return roots_and_stems

def deduce_root_type(list_of_roots):
    root_and_type_dict = {}
    for pair in list_of_roots:
        if pair[1] == "Q" or len(pair[0]) == 4:
            root_and_type_dict[pair[0]] = "Quad"
        elif pair[1] == "III":
            if pair[0].find('y') == 1:
                root_and_type_dict[pair[0]] = "III-2-y"
            elif pair[0].find('y') == 2:
                root_and_type_dict[pair[0]] = "III-3-y"
            elif pair[0].find('w') == 2:
                root_and_type_dict[pair[0]] = "III-3-w"
            elif pair[0].find('l') == 2:
                root_and_type_dict[pair[0]] = "III-3-l"
            elif pair[0].find('r') == 2:
                root_and_type_dict[pair[0]] = "III-3-r"
            else:
                root_and_type_dict[pair[0]] = "III-strong"
        elif pair[1] == "II":
            if pair[0].find('y') == 1:
                root_and_type_dict[pair[0]] = "II-2-y"
            elif pair[0].find('y') == 2:
                root_and_type_dict[pair[0]] = "II-3-y"
            elif pair[0].find('w') == 2:
                root_and_type_dict[pair[0]] = "II-3-w"
            elif pair[0].find('l') == 2:
                root_and_type_dict[pair[0]] = "II-3-l"
            elif pair[0].find('r') == 2:
                root_and_type_dict[pair[0]] = "II-3-r"
            else:
                root_and_type_dict[pair[0]] = "II-strong"
        elif pair[1] == "I":
            if pair[0].find('y') == 1:
                root_and_type_dict[pair[0]] = "I-2-y"
            elif pair[0].find('y') == 2:
                root_and_type_dict[pair[0]] = "I-3-y"
            elif pair[0].find('w') == 1:
                root_and_type_dict[pair[0]] = "I-2-w"
            elif pair[0].find('w') == 2:
                root_and_type_dict[pair[0]] = "I-3-w"
            elif pair[0].find('l') == 2:
                root_and_type_dict[pair[0]] = "I-3-l"
            elif pair[0].find('r') == 2:
                root_and_type_dict[pair[0]] = "I-3-r"
            else:
                root_and_type_dict[pair[0]] = "I-strong"
        elif pair[0] == "ʔmr":
            root_and_type_dict[pair[0]] = "ʔmr"
        elif pair[0] == "ʔzl":
            root_and_type_dict[pair[0]] = "ʔzl"
        else:
            print("No type was deduced for the root {0}. Continuing...".format(pair[0]))
            continue

    return root_and_type_dict

def change_root_format(root_and_types):
    formatted_roots_and_types = []
    for root, tp in root_and_types.items():
        numbered_consonants = {}
        i = 0
        while i < len(root):
            numbered_consonants["C{0}".format(i + 1)] = root[i]
            i += 1
        formatted_roots_and_types.append((numbered_consonants, tp))
    return formatted_roots_and_types
    

    
def apply_constructed_patterns(constructed_patterns, directory):
    paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            paths.append(os.path.join(root, file))
    paths = [path for path in paths if ".txt" in path]
    return paths


def construct_patterns(patterns, deduced_roots_with_types):
    constructed_patterns = []
    for entry in deduced_roots_with_types:
            print(entry)
            if entry[1] in patterns.keys():
                pattern = patterns[entry[1]]    
                for match in re.finditer(r"(C(\d))", pattern):
                    pattern = re.sub(match.group(0), entry[0][match.group(0)], pattern)
                constructed_patterns.append(pattern)
    return constructed_patterns

if __name__ == "__main__":
    patterns = read_patterns("../data/raw_data/data_for_scripts/patterns.txt")
    print("Provide the path to your roots file")
    roots_file = input()
    roots_and_stems_list = read_roots_and_stems(roots_file)
    deduced_roots = deduce_root_type(roots_and_stems_list)
    formatted_roots = change_root_format(deduced_roots)
    substituted_patterns = construct_patterns(patterns, formatted_roots)

    dirty = []
    for root, root_type in deduced_roots.items():
        dirty.append(root)

    count = 0

    with open("../data/derived_data/constructed_patterns.txt", "w") as file:
        for pattern in substituted_patterns:
            file.write(dirty[count])
            file.write(" ")
            file.write(pattern)
            file.write("\n")
            count += 1



    for entry in roots_and_stems_list:
        print(entry)

    for item in formatted_roots:
        print(item)

    for root, root_type in deduced_roots.items():
        print(root, root_type)

    for pattern in substituted_patterns:
        print(pattern)
