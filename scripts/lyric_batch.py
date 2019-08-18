"""
Runs all lyrics files within a directory through the CMU dictionary
and returns separate lists of individual words
(with the specific syllable number given) and the stress value of
the associated syllable.

Modified by Joseph VanderStel; based on work by Adam Waller.
"""

import os
import csv
import string
import itertools
import emphasis_script

for f in os.listdir('C:/Python27/checked'):
    if f.endswith('.txt'):
        base = os.path.basename(f)
        title = os.path.splitext(base)[0]
        emphasis_file = open('C:/Python27/checked/'+title+'_emphasis.csv','wb') #creates output file called 'title_emphasis.csv'
        emphasis_wr = csv.writer(emphasis_file)

        lyric_list = []
        print title

        with open('C:/Python27/checked/'+title+'.txt','rb') as f: #generates list of words in lyric file, stripping out spaces & line markers
            for line in f:
                line_x = line.rstrip() #removes spaces & line markers
                line_y = line_x.translate(string.maketrans("",""), string.punctuation) #removes punctuation
                line_z = line_y.upper() #make uppercase for searching in dictionary
                lyric_list.append(line_z.split()) #enters in each edited line as a separate list

        lyric_list_flat =  list(itertools.chain.from_iterable(lyric_list)) #flattens overall list

        for word in lyric_list_flat:  #adds row consisting of word & parsed dictionary entry [syllabic emphases] using word as key
            emph_list = emphasis_script.dictionary[word]
            for i in range(len(emph_list)):
                emphasis_wr.writerow([emph_list[i],word+'['+str(i+1)+']'])
