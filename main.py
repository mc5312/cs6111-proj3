import sys
import csv
import itertools

fname, min_sup, min_conf = None, None, None

L = dict() # Dict of large itemsets
C = dict() # Dict of itemset candidates
transactions, num_transaction = [], 0

def load_dataset():
    """
    Load transactions from CSV
    """
    global transactions
    global num_transaction
    with open(fname, newline='') as datafile:
        reader = csv.reader(datafile, delimiter=',')
        for r in reader:
            transactions += [r]
    num_transaction = len(transactions)


def get_initial_itemset():
    """
    Generate L[1], which contains frequent 1-itemsets 
    """
    global L
    
    L[1] = dict()
    for t in transactions:
        for item in t:
            L[1][item] = (L[1][item] + 1) if (item in L[1]) else 1

    L[1] = {k: v / num_transaction for k, v in L[1].items()}
    L[1] = {k: v for k, v in L[1].items() if (v >= min_sup)}
    L[1] = {tuple([k]): v for k, v in sorted(L[1].items(), key=lambda x: x[0])}


def apriori_gen(itemsets):
    """
    Generate C[k], candidate itemsets, with prune step

    param itemsets: L[k-1], last itemsets
    """
    global C
   
    k = len(itemsets[0]) + 1
    C[k] = list()
    
    for i in range(len(itemsets)):
        for j in range(i+1, len(itemsets)):
            if (k == 2) or (itemsets[i][:k-2] == itemsets[j][:k-2]):
                if (itemsets[i][k-2] < itemsets[j][k-2]):
                    C[k] += [itemsets[i] + tuple([itemsets[j][k-2]])]
    
    # === implementation of prune step
    candidate_sets = C[k].copy()
    for c in candidate_sets:
        for s in list(itertools.combinations(set(c), k-1)):
            if s not in itemsets:
                C[k].remove(c)
                break
    return C[k]


def run_apriori():
    """
    Run Algorithm Apriori to generate large itemsets
    """
    global L
    get_initial_itemset()

    k = 2
    while len(L[k-1]) > 0:
        C[k] = apriori_gen(list(L[k-1].keys()))
        L[k] = dict()
        
        for t in transactions:
            C_t = [c for c in C[k] if set(c).issubset(t)]
            for c in C_t:
                L[k][c] = (L[k][c] + 1) if (c in L[k]) else 1
        
        L[k] = {k: v / num_transaction for k, v in L[k].items()}
        L[k] = {k: v for k, v in L[k].items() if (v >= min_sup)}

        k += 1


def output_result():
    """
    Generate output to 'output.txt'
    """
    f = open("output.txt", "w")
    
    # === Output frequent itemsets
    f.write("==Frequent itemsets (min_sup={:,.0%})\n".format(min_sup))
    freq_itemsets = dict()
    for size, itemsets in L.items():
        for itemset, sup in itemsets.items():
           freq_itemsets[itemset] = sup
    
    # sort by decreasing support
    freq_itemsets = {k: v for k, v in reversed(sorted(freq_itemsets.items(), key=lambda x: x[1]))}
    for k, v in freq_itemsets.items():
        f.write(("[{}], {:,.0%}\n".format(','.join(k), v)))
    f.write("\n")

    # === Output high-confidence association rule
    f.write("==High-confidence association rules (min_conf={:,.0%})\n".format(min_conf))

    rule = dict()
    for k in range(2, len(L)):
        for itemset in list(L[k].keys()):
            for rhs_idx in reversed(range(len(itemset))):
                lhs = tuple([x for i, x in enumerate(itemset) if i != rhs_idx])
                rhs = tuple([itemset[rhs_idx]])
                sup = L[k][itemset]
                conf = sup / L[k-1][lhs]
                if conf >= min_conf:
                    rule[(lhs, rhs)] = (conf, sup)
    
    # sort by decreasing confidence
    rule = {k: v for k, v in reversed(sorted(rule.items(), key=lambda x: x[1][0]))}
    for k, v in rule.items():
        f.write(("[{}] => [{}] (Conf: {:,.1%}, Supp: {:,.0%})\n".format(','.join(k[0]), ','.join(k[1]), v[0], v[1])))

    f.close()


if __name__ == "__main__":
    fname, min_sup, min_conf = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    
    load_dataset()
    run_apriori()
    output_result()