


# In the hapcut input file, each line has haplotype information from a single fragment. For each variant covered by the fragment, information about the variant-id and allele is recorded as follows:
# 
# Column 1 is the number of blocks (consecutive set of variants covered by the fragment).
# Column 2 is the fragment id.
# Column 3 is the offset of the first block of variants covered by the fragment followed by the alleles at the variants in this block.
# Column 4 is the sequence of alleles at variants in the first block
# Column 5 is the offset of the second block of variants covered by the fragment followed by the alleles at the variants in this block.
# ...
# 
# The last column is a string with the quality values (Sanger fastq format) for all the alleles covered by the fragment (concatenated for all blocks).
# 
# For example, if a read/fragment covers SNPs 2,3 and 5 with the alleles 0, 1 and 0 respectively, then the fragment will be:
# 
# 2 read_id 2 01 5 0 AAC
# 
# Here AAC is the string corresponding to the quality values at the three alleles (encoded using char(QV+33)). The encoding of 0/1 follows the VCF format, 0 is reference and 1 is alternate.
# 
# The offset for each variant corresponds to the index of the variant in the VCF file (one-based)