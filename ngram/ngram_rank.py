import sys
import re

def rank(fname):
    order_to_sketch = {}
    order_to_prob = {}

    #org_to_num = {}

    order = 1
    with open(fname) as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):
            if (i+2) >= len(lines):
                break

            sketch = lines[i].strip()
            result = lines[i+2].strip()
            order_to_sketch[order] = sketch
            nums = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", result) 
            p1 = float(nums[2])
            p2 = float(nums[4])
            #print sketch,' [PROB]', result, p2, nums[4]
            order_to_prob[order] = p2
    #        if sketch in org_to_num:
    #            org_to_num[sketch] = org_to_num[sketch] + 1
    #        else:
    #            org_to_num[sketch] = 1

            order += 1

    ###output ranking#############
    pos = 1
    sort_map = sorted(order_to_prob.items(), key=lambda x:x[1])
    for (org_order, prob) in sort_map:
        sk = order_to_sketch[org_order]
        #print sk, ' Current pos:', pos, ' org pos:', org_order, ' Perplexity:', prob 
        print sk
        #assert sk in org_to_num
        #org_to_num[sk] = org_to_num[sk] - 1
        #pos += 1

    #for key in org_to_num:
    #    value = org_to_num[key]
    #    assert value == 0
     

def main(argv):
    fname = argv[0]
    #print 'file name:', fname
    rank(fname)

if __name__ == "__main__":
    main(sys.argv[1:])
