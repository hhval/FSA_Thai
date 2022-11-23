#!/usr/bin/python

"""%prog [--help] [category file] [input file] [output file]

This project implements a finite state automaton (FSA) that identifies syllables in Thai text."""

import sys

fsa = {
0: [('V1', 1), ('C1', 2)],
1: [('C1', 2)],
2: [('C2', 3), ('V2', 4), ('T', 5), ('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)],
3: [('V2', 4), ('T', 5), ('V3', 6), ('C3', 9)],
4: [('T', 5), ('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)],
5: [('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)],
6: [('C3', 9), ('V1', 7), ('C1', 8)],
7: 1,
8: 2,
9: 0
}

def get_cat2chars(category_file):
    categorydict = {}
    for line in category_file:
        category = line.split()
        categorydict[category[0]] = category[1:]
    return categorydict

def syllable_breaker(inputtext,cat2chars):
    segmented = ''
    current_state_index = 0
    finishedlines = ''
    
    for line in inputtext:
        for char in line:
            for (category, to_state_index) in fsa[current_state_index]:
                if char in cat2chars[category]:
                    current_state_index = to_state_index
                    break

            if current_state_index == 7 or current_state_index == 8:
                segmented = segmented + ' ' + char
                current_state_index = fsa[current_state_index]

            elif current_state_index == 9:
                segmented = segmented + char + ' '
                current_state_index = fsa[current_state_index]

            else:
                segmented = segmented + char
        
        if finishedlines == '':
            finishedlines = segmented
        else:
            finishedlines = finishedlines + '\n' + segmented
        segmented = ''

    return finishedlines
        
def main():
    categoryfile = sys.argv[1]
    inputfile = sys.argv[2]
    outputfile = sys.argv[3]

    with open(categoryfile, 'r', encoding='utf8') as f: 
        catlines = f.readlines()
    categorykeys = get_cat2chars(catlines)
    
    with open(inputfile, 'r', encoding='utf8') as f: 
        inputlines = f.readlines()
    segmentedtext = syllable_breaker(inputlines,categorykeys)

    with open(outputfile, 'w', encoding='utf8') as f: 
        f.write(segmentedtext)

if __name__ == "__main__":
    main()
    