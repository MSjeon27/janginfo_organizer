import argparse

def main():

    parser = argparse.ArgumentParser(description=(
        "Remane the tig name of genome fasta file which have complicated tig names"
        ))
    parser.add_argument('Input', metavar='i', help="Input fasta")
    parser.add_argument('-o', '--out', metavar='o', help="Output file name", default='tig_rename.fa')
    args = parser.parse_args()

    # Set tig directory
    tig_dict = dict()

    # Get Sequence information
    with open(args.Input, 'r') as ipf:
        for tig in ipf.read().split('>')[1:]:
            head = tig.split('\n')[0]
            seq = ''.join(tig.split('\n')[1:])
            tig_dict[head] = seq

    # Reform the sequence information
    n = 1
    out_dict = dict()
    for tig in tig_dict.keys():
        head = 'tig{}\t{}'.format(n, tig)
        seq = tig_dict[tig]
        out_dict[head] = seq
        n += 1

    # Generate output file
    with open(args.out, 'w') as opf:
        for key in out_dict.keys():
            opf.write('>' + key + '\n')
            while len(out_dict[key]) >= 80:
                if len(out_dict[key]) > 80:
                    opf.write(out_dict[key][:80] + '\n')
                elif len(out_dict[key]) == 80:
                    opf.write(out_dict[key][:80])
                out_dict[key] = out_dict[key][80:]
            else:
                opf.write(out_dict[key] + '\n')