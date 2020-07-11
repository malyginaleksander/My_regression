import csv

# Open a file: file

f = open('./txt_files/1.txt', mode='r')

# read all lines at once
all_of_it = f.read()
# print(all_of_it)

x = f.readlines()
print (x)
s = []

for i in x:
    s.append (all_of_it)

print(s)

csvex  = csv.writer(open("txt_export", "w"),  delimiter = "\t", quoting = csv.QUOTE_ALL)
csvex.writerow(s)

f.close()
