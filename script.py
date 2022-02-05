# importing pandas library
import pandas as pd

# importing tracemalloc for calculating memory
import tracemalloc 

# importing time for calculating time
import time

# initialising memory start 
mem_start = tracemalloc.start()
time_start = time.time()
# converting text file into a csv
df1 = pd.read_csv("find_words.txt", header=None, names=['eng'])
df1.to_csv('find_word.csv')

#naming the columns of dictionary file of csv format
df2 = pd.read_csv("french_dictionary.csv", header=None, names=['eng', 'french']);
# df2.columns = ['eng', 'french']
# print(df1.head())
# print(df2.head())

#merging the or simply intersecting the two csv files
df = pd.merge(df1, df2, how='inner', on="eng")

# making key value pairs for each of the words of english to french
dictionary = dict(zip(df.eng, df.french))
# print(dictionary)

# opening the main content file
f = open("t8.shakespeare.translated.txt" , "r")
filedata = f.read()
f.close()



changed = []

for key in dictionary:
    lower = key.lower()
    upper = key.upper()
    title = key.title()
    count1 = filedata.count(lower)
    count2 = filedata.count(upper)
    count3 = filedata.count(title)
    if(count1>0):
        filedata = filedata.replace(lower, dictionary[lower])
    if(count2>0):
        filedata = filedata.replace(upper,dictionary[lower].upper())
    if(count3>0):
        filedata = filedata.replace(title,dictionary[lower].title())  
    if(count1 > 0 or count2 > 0 or count3 > 0):
        changed.append({"word":lower, "occurance": count1+count2+count3})      

time_end = time.time()
mem_end = tracemalloc.stop()

# writing into actual file
f = open("t8.shakespeare.txt", "w")
f.write(filedata)
f.close()

total_time = time_end - time_start

f = open("performance.txt", "a")
minutes = total_time/60
seconds = total_time%60
f.write(f"Time to process: {int(minutes)} minutes {int(seconds)} seconds\n" )
f.write(f"Memory used: {int(tracemalloc.get_traced_memory()[1]*1e-6)} MB")

f = open("frequency.csv","a")
f.write("English Word,French Word,Frequency\n")
for obj in changed:
  stri = f"{obj['word']},{dictionary[obj['word']]},{obj['occurance']}\n"
  f.write(stri + "\n")
f.close()