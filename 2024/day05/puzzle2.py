import os, sys
from collections import defaultdict

def is_valid(rules, pages):
    for i in range(len(pages)):
        page = pages[i]

        if page in rules:
            required_pages = rules[page]

            for required_page in required_pages:
                if required_page in pages[i:]:
                    return False
            
    return True
    

def reorder(rules, pages):
    check = True
    while check:
        check = False

        i = 0
        while i < len(pages):
            page = pages[i]

            if page in rules:
                required_pages = rules[page]

                for j in range(i+1, len(pages)):
                    if pages[j] in required_pages:                        
                        pages = pages[0:i] + [pages[j]] + pages[i:j] + pages[j+1:]
                        check = True
            
            i = i + 1
            
    return pages

def solve(filename):
    lines = read_file_lines(filename)

    rules = defaultdict(set)
    ans = 0

    for line in lines:
        if "|" in line:
            (l,r) = line.split("|")

            rules[int(r)].add(int(l))
        elif line:
            parts = line.split(",")
            pages = [int(x) for x in parts]

            if not is_valid(rules, pages):
                fixed = reorder(rules, pages)
                middle = fixed[len(fixed)//2]
                ans = ans + middle

    
    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')