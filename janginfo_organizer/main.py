import argparse
from Bio import SeqIO
from Bio import Seq
import pandas as pd

def main():

    parser = argparse.ArgumentParser(description=(
        ""
        ))
    parser.add_argument('fasta', metavar='f', help="Input fasta file")
    parser.add_argument('genbank', metavar='g', help="Input gbk file")
    parser.add_argument('sernum', metavar='s', help="""
    Serial number format
    ex) F-Deb-han-1
    (Fungi-Debaryomyces-hansenii-1st sample)
    """)
    parser.add_argument('-o', '--out', metavar='o', default='fun_organize.csv', help="Output file name")
    args = parser.parse_args()

    # Import input annotation file into dictionary
    inp_dict = dict() # Set input dictionary
    n = 1
    # Get information
    record_iterator = SeqIO.parse(args.genbank, "genbank")
    for rec in record_iterator:
        if rec.features:
            for feature in rec.features:
                # print(feature)
                # print(dir(feature))
                # Get information only about cds region
                if feature.type == 'CDS':
                    # Set serial number of gene
                    sernum = "{}-{}".format(args.sernum, str(n).zfill(6))
                    n += 1
                    # Extract contig information
                    tig = rec.name
                    # Extract Locus ID
                    locid = feature.qualifiers["locus_tag"][0]
                    # Extract position information
                    start_pos = int(feature.location.start) + 1
                    end_pos = int(feature.location.end)
                    # Extract strand information
                    strand = feature.location.strand
                    # Extract gene name
                    try:
                        gene = feature.qualifiers["gene"][0]
                    except KeyError:
                        gene = 'hypothetical protein'
                    # Extract product information
                    prod = feature.qualifiers["product"][0]
                    # Extract sequence information (protein)
                    prot_seq = feature.qualifiers["translation"][0]
                    # print(feature.location.extract(rec).seq)
                    inp_dict[sernum] = [tig, locid, start_pos, end_pos, strand, gene, prod, prot_seq]

    # Get contig sequence information from fasta file
    fasta_dict = dict()
    with open(args.fasta, 'r') as ff:
        for tig in ff.read().split('>')[0:]:
            tig_name = tig.split('\n')[0]
            tig_seq = ''.join(tig.split('\n')[1:])
            fasta_dict[tig_name] = tig_seq

    # Set outdict and make final output dictionary
    out_dict = dict()
    # Get nucleotide cds sequence
    for key in inp_dict.keys():
        tig = inp_dict[key][0]
        start_pos = int(inp_dict[key][2])
        end_pos = int(inp_dict[key][3])
        strand = inp_dict[key][4]
        nuc_seq_pre = fasta_dict[tig][start_pos - 1 : end_pos + 1]
        # Check the orientation of cds sequence
        if strand == -1:
            tempt_seq = Seq.Seq(nuc_seq_pre)
            nuc_seq = str(tempt_seq.reverse_complement())
        else:
            nuc_seq = nuc_seq_pre
        out_dict[key] = inp_dict[key]
        out_dict[key].append(nuc_seq)

    # Create empty dataframe
    df = pd.DataFrame(columns=['샘플 일련번호', '위치', '유전자 일련번호', 'Locus ID', '시작', '끝', '염기 방향', 'Gene', 'Product', '기능성', '안정성', '단백질 서열', '염기 서열'])

    # Create output file
    for key in out_dict.keys():
        tig = out_dict[key][0]
        locid = out_dict[key][1]
        start_pos = out_dict[key][2]
        end_pos = out_dict[key][3]
        strand = out_dict[key][4]
        if strand == -1:
            strand_chr = "-"
        else:
            strand_chr = "+"
        gene = out_dict[key][5]
        Product = out_dict[key][6]
        prot_seq = out_dict[key][7]
        nuc_seq = out_dict[key][8]
        df = df.append(pd.DataFrame(
            [[args.sernum, tig, key, locid, start_pos, end_pos, strand_chr, gene, Product, '', '', prot_seq, nuc_seq]],
            columns=['샘플 일련번호', '위치', '유전자 일련번호', 'Locus ID', '시작', '끝', '염기 방향', 'Gene', 'Product', '기능성', '안정성', '단백질 서열', '염기 서열']
        ), ignore_index=True)

    df.to_csv(args.out, encoding='utf-8-sig', index=None)