#runall
#2023-12-06
#Download data
#proteomes.txt is a text file with ftp adresses
#to desired proteomes.
#input="proteomes.txt"

#while IFS= read -r line
#do
#	wget "$line"
#done < "$input"

#Unzip gz archives
#gunzip UP*

#concatenate fastas to one file for easier
#handling.
#cat UP* >> all_proteomes.fasta

#download LG model
#wget http://www.atgc-montpellier.fr/download/datasets/models/lg_LG.PAML.txt

#calculate amino acid frequencies.
#python3 ../../bin/aa_freq.py all_proteomes.fasta > aa_freq.txt

#Modify the LG PAML file and HMM (using YopJ from uniprot for now)

python3 ../../bin/modify_hmm.py aa_freq.txt lg_LG.PAML.txt ../../data/PF03421.hmm output_t0.1.hmm 0.1
python3 ../../bin/modify_hmm.py aa_freq.txt lg_LG.PAML.txt ../../data/PF03421.hmm output_t0.5.hmm 0.5
python3 ../../bin/modify_hmm.py aa_freq.txt lg_LG.PAML.txt ../../data/PF03421.hmm output_t0.01.hmm 0.01
python3 ../../bin/modify_hmm.py aa_freq.txt lg_LG.PAML.txt ../../data/PF03421.hmm output_t0.7.hmm 0.7

python3 ../../bin/modify_hmm.py aa_freq.txt lg_LG.PAML.txt ../../data/PF03421.hmm output_t0.2.hmm 0.2
python3 ../../bin/modify_hmm.py aa_freq.txt lg_LG.PAML.txt ../../data/PF03421.hmm output_t0.4.hmm 0.4

