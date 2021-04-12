#!/usr/bin/env python3

import sys,fnmatch,gzip

fragmentsFile=sys.argv[1]
phasedvcf = sys.argv[2]
truthvcf=sys.argv[3]

print("Hi there!")

def getTruth(vrows,row2region,region2truth):
    chrA=""
    chrB=""
    for row in vrows:
        if row in row2region:
            region = row2region[row]
        else:
            print("row isn't in vcf??? ",row)
            # row isn't in the vcf, something is really wrong.
            
        if region in region2truth:
            (alleleA,alleleB) = region2truth[region]
        else:
            alleleA='?'
            alleleB='?'
            
        chrA+=alleleA
        chrB+=alleleB
    
    return chrA,chrB
        
def buildRow2Region(phasedvcf):
    row = 1
    row2region=dict()
    with open(phasedvcf) as pin:
        for line in pin:
            line = line.strip()
            if line.startsWith("#"): continue
            
            fields = line.split("\t")
            region=fields[1]
            row2region[row]=region
            row+=1
    
    return row2region
  
def buildRegion2Truth(truthvcf):
    region2truth=dict()
    with gzip.open(truthvcf,'r') as tin:
        for line in tin:
            line = line.strip()
            if line.startsWith("#"): continue
             
            fields = line.split("\t")
            region = fields[1]
            phasestr = fields[9]
            phasefields = phasestr.split(":")
            truthstr=phasefields[0]
            alleleA,alleleB = truthstr.split("|")
            region2truth[region]=(alleleA,alleleB)
           
    return region2truth

def parseFragmentLine(line):
    vrows=[]
    phase=""
    fields = line.split(" ")
    numblocks = int(fields[0])
    remainder = fields[5:-1]
    it = iter(remainder)
    for x in it:
        vrows.append[x]
        allele=next(it)
        phase+=allele
        
    return vrows,phase
    
def match(fragphase,truephaseA,truePhaseB):
    # 1?1 should match 101 111
    f1 = fnmatch.filter([fragphase],truephaseA)
    f2 = fnmatch.filter([fragphase],truephaseB)
    if len(f1)>0 or len(f2) > 0:
        return True
    else:
        return False     

# Read phased output and build row2region table
print("Build row2region...")
row2region = buildRow2Region(phasedvcf)

# Read truthset vcf and build region2phase table
print("Build region2truth...")
region2truth = buildRegion2Truth(truthvcf)

print("Scan fragments file...")
matchCount = 0
mismatchCount = 0
with open(fragmentsFile) as fin:
    for line in fin:
        vrows,fragphase = parseFragmentLine(line)
    
        truephaseA,truephaseB = getTruth(vrows,row2region,region2truth)
    
        if match(fragphase,truephaseA,truePhaseB):
            matchCount+=1
        else:
            mismatchCount+=1


    print("Match count: ",matchCount)
    print("Mismatch count: ",mismatchCount)
    

