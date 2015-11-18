#!/usr/bin/env python
'''
Formatting the results of the dataset tests so they can be compared
'''

if __name__ == '__main__':
    resultsFileName = "20NewsCorpusResults.csv"
    resultsScoreFileName = resultsFileName[:-4] + "_Scores.csv"
    fin = open(resultsFileName, 'r')
    data = fin.readlines()
    fin.close()
    fout = open(resultsScoreFileName, 'w')
    fout.write("Filename,SciKit-tfidf,SciKit-lsa,SciKit-lda,GenSim-tfidf,"
               "GenSim-lsa,GenSim-lda\n")
    j = 1  # Skip name of columns
    for i in range(1, ((len(data) / 6) + 1)):  # For each set of 6 results
        l = data[j].split(',')
        matches = {}
        for k in range(6):  # Save document name with number for common docs
            info = data[j + k].split(',')
            if info[3] in matches:
                matches[info[3]] += 5
            else:
                matches[info[3]] = 5

            if info[5] in matches:
                matches[info[5]] += 4
            else:
                matches[info[5]] = 4

            if info[7] in matches:
                matches[info[7]] += 3
            else:
                matches[info[7]] = 3

            if info[9] in matches:
                matches[info[9]] += 2
            else:
                matches[info[9]] = 2

            if info[11] in matches:
                matches[info[11]] += 1
            else:
                matches[info[11]] = 1

        for num in matches:  # Divide the matches by 90 (The number of points)
            matches[num] /= 90.0
        line = file
        for k in range(6):  # Get the info and write it out to the score .csv
            info = data[j + k].split(',')
            tool = info[1]
            model = info[2]
            score = matches[info[3]] * (float(info[4]) / 100)
            line += "," + str(score)
        fout.write(line + '\n')
        j += 6
    fout.close()
