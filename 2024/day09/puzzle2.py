import os, sys

def find_gap_index(gaps, fsize, findex):
    for j in range(len(gaps)):
        (gindex, gsize) = gaps[j]
        if gindex > findex:
            continue

        if gsize >= fsize:
            return j
    
    return None

def solve(filename):
    lines = read_file_lines(filename)
    line = lines[0]

    files = list()
    gaps = list()

    index = 0

    for i in range(len(line)):
        num = int(line[i])
        if (i % 2) == 0:
            fileid = i//2
            files.append((index, num, fileid))
        else:
            gaps.append((index, num))

        index = index + num

    i = len(files) - 1
    while i > 0:
        (findex, fsize, fid) = files[i]

        gaps_index = find_gap_index(gaps, fsize, findex)
        if gaps_index is None:
            i = i - 1
            continue

        (gindex, gsize) = gaps[gaps_index]

        moveFile = False
        if gsize == fsize:
            gaps.pop(gaps_index)
            moveFile = True
        elif gsize > fsize:
            gaps[gaps_index] = (gindex+fsize, gsize-fsize)
            moveFile = True

        if moveFile:
            files.pop(i)
            moved = False
            for k in range(len(files)):
                if files[k][0] > gindex:
                    files.insert(k, (gindex, fsize, fid))
                    moved = True
                    break
            if not moved:
                files.append((gindex, fsize, fid))
        else:
            i = i - 1
    
    ans = 0
    for i in range(len(files)):
        (findex, fsize, fid) = files[i]
        for j in range(findex, findex+fsize):
            ans = ans + (j * fid)

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')