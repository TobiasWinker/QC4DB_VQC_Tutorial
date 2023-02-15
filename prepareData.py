import csv
from math import pi

# load data from the benchmark file
with open('benchmark.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
    
# create set for tables names
tables = set()

# add all occurring table name
for row in data:
    tables.update(row[0:4])

# convert to list to names to indices
tables = list(tables)

with open('data.csv', 'w') as output:
    for row in data:
        # convert names to values in interval [0,pi]
        temp = [tables.index(x)/(len(tables)-1)*pi for x in row[0:4]]
        # select execution times (alternative use intermediates )
        values = [float(x) for x in row[4:(4+15)]]
        # find best value
        best = min(i for i in values if i > 0)
        # calculate rewards
        for x in values:
            if x<0:     # cross join 
                temp.append(0)
            else:
                temp.append(best/x)
        # pad to 16 values (next power of 2)
        temp.append(0)
        # write to file
        output.write(",".join(str(x) for x in temp))
        output.write("\n")
