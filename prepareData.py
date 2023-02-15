import csv
from math import pi

# Load data from the benchmark file
with open('benchmark.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
    
# Create set for tables names
tables = set()

# Add all occurring table name
for row in data:
    tables.update(row[0:4])

# Convert to list to names to indices
tables = list(tables)

with open('data.csv', 'w') as output:
    for row in data:
        # Convert names to values in interval [0,pi]
        temp = [tables.index(x)/(len(tables)-1)*pi for x in row[0:4]]
        # Select execution times (alternative use intermediates )
        values = [float(x) for x in row[4:(4+15)]]
        # Find best value
        best = min(i for i in values if i > 0)
        # Calculate rewards
        for x in values:
            if x<0:     # cross join 
                temp.append(0)
            else:
                temp.append(best/x)
        # Pad to 16 values (next power of 2)
        temp.append(0)
        # Write to file
        output.write(",".join(str(x) for x in temp))
        output.write("\n")
