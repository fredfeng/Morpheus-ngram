import sys
import re

def rank(fname):
    prob_to_sketch = {}
    sketch_to_order = {}
    probs = []

    order = 1
    with open(fname) as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):
            if (i+2) >= len(lines):
                break

            sketch = lines[i].strip()
            result = lines[i+2].strip()
            sketch_to_order[sketch] = order
            nums = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", result) 
            p1 = float(nums[2])
            p2 = float(nums[4])
            #print sketch,' [PROB]', result, p2, nums[4]
            prob_to_sketch[p2] = sketch
            probs.append(p2)
            order += 1

    ###output ranking#############
    pos = 1
    #print probs
    probs.sort()
    #print probs
    for p in probs:
        sk = prob_to_sketch[p]
        org_order = sketch_to_order[sk]
        print sk, ' Current pos:', pos, ' org pos:', org_order, ' Perplexity:', p 
        pos += 1
     

def main(argv):
    fname = argv[0]
    print 'file name:', fname
    rank(fname)

if __name__ == "__main__":
    main(sys.argv[1:])
