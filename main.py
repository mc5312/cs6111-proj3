import sys

fname, min_sup, min_conf = None, None, None



if __name__ == "__main__":
    fname, min_sup, min_conf = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    print(fname, min_sup, min_conf)