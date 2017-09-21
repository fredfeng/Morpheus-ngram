import sys
import re
import os

# Map from new to old sentences
new_old_map = {}

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
        #print sk
        #print new_old_map[sk]
        assert sk in new_old_map,(sk)
        for item in new_old_map[sk]:
            print item


        #assert sk in org_to_num
        #org_to_num[sk] = org_to_num[sk] - 1
        #pos += 1

    #for key in org_to_num:
    #    value = org_to_num[key]
    #    assert value == 0
     
# Clean file by removing FOL components
def clean_file(fname):
    #print('Clean_file: ' + fname)
    with open(fname) as f:
        lines = f.readlines()
        for line in lines:
            assert len(line.strip()) > 0
            # l(a,b).(/ a b)
            new_line = re.sub(r'l\(a,b\).\(..? a b\)', '', line.strip()).strip()
            assert len(new_line.strip()) > 0 , (line.strip() + '|||| ' + new_line)
            sentences = []
            #print line.strip() + "$$$" + new_line
            if new_line in new_old_map:
                sentences = new_old_map[new_line]
                sentences.append(line.strip())
                new_old_map[new_line] = sentences
            else:
                sentences.append(line.strip())
                new_old_map[new_line] = sentences

    ##Save the new sentences to a tmp file: tmp_file.txt
    #print len(new_old_map.keys())
    thefile = open('tmp_file.txt', 'w')
    for item in new_old_map.keys():
        print>>thefile, item

    return

# Generate the probabilites of each sentences using ngram
# ngram -lm 2gram_v2.lm -ppl tmp_file.txt -debug 1 > tmp_ngram.txt
def ngram_rank(fname):
    os.system("ngram -lm 2gram_final.lm -ppl tmp_file.txt -debug 1 > tmp_ngram.txt")
    return

# Recover the sentences resp. to the new ranking
def recover_sentences():
    return

def main(argv):
    fname = argv[0]
    #print 'file name:', fname
    #rank(fname)
    clean_file(fname)
    ngram_rank('tmp_file.txt')
    os.remove('tmp_file.txt')
    rank('tmp_ngram.txt')
    os.remove('tmp_ngram.txt')

if __name__ == "__main__":
    main(sys.argv[1:])
