#Takes input LG matrix and modifies given aa frequencies
import numpy as np
import sys
from scipy.linalg import expm

def read_aa_frequencies(file_path):
    with open(file_path, 'r') as file:
        return [float(line.strip()) for line in file]

def reorder_matrix(matrix, current_order, target_order):
    index_map = [current_order.index(aa) for aa in target_order]
    reordered_matrix = matrix[:, index_map][index_map]
    return reordered_matrix

def read_lg_model(file_path):
    rates = []
    with open(file_path, 'r') as file:
        for line in file:
            rates.extend([float(rate) for rate in line.strip().split()])
    return rates

def convert_to_matrix(rates):
    matrix = np.zeros((20,20))
    index = 0
    for i in range(1,20):
        for j in range(i):
            matrix[i,j] = matrix[j,i] = rates[index]
            index += 1
    return matrix

def format_fields(fields, probs):
    formatted_fields = "{:>7}   ".format(fields[0])
    formatted_fields += "  ".join("{:>3.5f}".format(p) for p in probs)
    return formatted_fields

def read_hmm(file_path):
    with open(file_path, 'r') as file:
        #skip header
        start_reading = False
        match_emissions = []

        for line in file:
            if line.startswith('HMM'):
                start_reading = True
                continue
            if line.startswith('//'):
                break
            if start_reading and not line.isspace():
                fields = line.strip().split()
                #Check if the line representsa match
                if fields[0].isdigit():
                    #convert the log probabilities to regular probabilities
                    probabilities = [np.exp(-float(p)) for p in fields[1:21]]
                    match_emissions.append(probabilities)
        return match_emissions

def convert_probabilities_to_log(probabilities):
    return [-np.log(p) if p>0 else sys.float_info.max for p in probabilities]

def write_modified_hmm(original_hmm, modified_em, output):
    with open(original_hmm, 'r') as original, open(output, 'w') as modified_hmm:
        start_modifying = False
        match_state_index = 0

        for line in original:
            if line.startswith('HMM'):
                start_modifying = True
                modified_hmm.write(line)
                continue
            if line.startswith('//'):
                modified_hmm.write(line)
                break
            if start_modifying and not line.isspace():
                fields = line.strip().split()
                last_five = None
                if fields[0].isdigit() and match_state_index < len(modified_em):
                    if last_five is None:
                        last_five = fields[-5:]

                    new_line = format_fields(fields, modified_em[match_state_index])
                    new_line += "      "
                    new_line += ' '.join(last_five) + '\n'
                    modified_hmm.write(new_line)
                    match_state_index += 1
                else:
                    modified_hmm.write(line)
            else:
                modified_hmm.write(line)

def main():
    #read data
    aa_frequencies = read_aa_frequencies(sys.argv[1])
    lg_rates = read_lg_model(sys.argv[2])

    #get frequencies from sums
    total = sum(aa_frequencies)
    normalized_frequencies = [freq / total for freq in aa_frequencies]
    
    #convert lg matrix into different format
    Q = convert_to_matrix(lg_rates)

    for i in range(20):
        Q[i,i] = -np.sum(Q[i,:])*normalized_frequencies[i]

 
    #exponentiate our Q to find P(t)
    t = 0.1
    P_t = expm(Q * t)

    #Reorder P_t since it's in a different order than the hmm
    current_order = ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V"]
    target_order = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y"]

    P_t_reordered = reorder_matrix(P_t, current_order, target_order)
    #read hmm
    hmm_emissions = read_hmm(sys.argv[3])
    modified = []
    #modify match states given our matrix
    for probs in hmm_emissions:
        modified_probs = np.dot(probs, P_t_reordered)
        #renormalize
        #modified_probs /= np.sum(modified_probs)
        modified.append(modified_probs)

    #write back into original HMM format.
    write_modified_hmm(sys.argv[3], modified, 'modified_hmm.hmm')

if __name__ == "__main__":
    main()
