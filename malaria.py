#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
malaria.py
Version: 1.00
Date: 2024-10-14
Name: Rebecka Antonsson

How my workflow connects to the FAIR principles:
Findable: The output file is stored in the current working directory, which is easy to locate. The script is stored on github
in the same folder as the input files, making it easy to find.
Accessible: The script can be run from any location as long as the input files are provided with correct paths. 
Interoperable: The script uses standard file formats (FASTA and tab-delimited text) that can be easily read by other bioinformatics tools.
The code is also well commented which makes it easier for others to follow and understand all parts of the code. File formats for inputfiles 
are standard. 
Reusable: The script is well-documented and can be reused for similar tasks with different input files. The license is MIT, 
which allows for free use and distribution. 

Motivation for version pinning:
The only dependencies used are sys, pathlib and os, which are all part of the standard library in Python. 
There is no need for version pinning in this case.
Since only standard libraries are used, the only thing that could possibly break the script in the future is if the python version changes.
But it is still not likley to affect anything, however you can never be sure and the script should be tested if a new python version is released.
"""

import sys
from pathlib import Path
import os

try:
    # Loading the content of malaria.blastx.tab into the variable f_bastx
    # Then reading it line by line into the variable f_blastx
    # f_blastx = open("/home/inf-35-2024/BINP16/Running_exercise1/malaria.blastx.tab","r") # IF RUNNED FROM SPYDER
    f_blastx = open(sys.argv[2],"r")
    header_blastx=f_blastx.readline() # reads the header so it dosent get into the l_blastx file
    if len(header_blastx.removesuffix("/n").split("\t"))!=17:
        raise Exception()
    l_blastx = f_blastx.readlines()   
    f_blastx.close()
    
    # For every line in l_blastx, take the id [0] and protein name [9]
    # put in dictionary with id as key and protein name as value
    id_proetin_dic = {}
    for blastx_line in l_blastx:
        blastx_line = blastx_line.split("\t") # split the string into columns divided by tab
        id_proetin_dic[blastx_line[0]]=blastx_line[9]
        
     
        
    # FASTA file
    
    # Loading the content of malaria.fna into the variable f_fasta
    # Then reading it line by line into the variable f_fasta
    #f_fasta = open("/home/inf-35-2024/BINP16/Running_exercise1/malaria.fna","r") # IF RUNNED FROM SPYDER 
    f_fasta = open(sys.argv[1],"r")
    if f_fasta.readline().startswith(">"): # only continue if the file is a FASTA file
        f_fasta.close()
        f_fasta = open(sys.argv[1],"r")
        l_fasta = f_fasta.readlines() # don't have header like blastx, so no reanline() needed 
        f_fasta.close()
    else:
        raise Exception()
    
    

    # Output file
    
    # Get the current working directory, so that the outputfile can be stored there
    
    current_working_directory=Path.cwd()
        
    # Instead of just adding the path with a +, 
    # this is a more robust way of joing the path 
    # (current working directory + the new file name)
    
    file_path = os.path.join(current_working_directory, "output.txt")
    
    output = open(file_path,"w")
    # for every line in l_fasta, get the headers and put them in the variable fasta_header
    for fasta_line in l_fasta:
        if fasta_line.startswith(">"):
            fasta_header = fasta_line.split("\t")[0][1:] # splits it into columns, and get the first column, and remove the >
            if id_proetin_dic[fasta_header]=="null":
                continue
            else:
                # Here insead of doing it to the variable write it to the output file
                fasta_and_protein = fasta_line.strip()+" "+str(id_proetin_dic[fasta_header])
                output.write(fasta_and_protein)
        else:
            output.write(fasta_line)
    output.close()

except Exception:
    print("There something wrong with one or both of the input files")
    sys.exit()
except IndexError:
    print("What I have tested so far: the input files where put in the wrong order")
    sys.exit() # Exit because then the program shouldn't run
except FileNotFoundError:
    print("The entered file does not exist")
    sys.exit()
 
