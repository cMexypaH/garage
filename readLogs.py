from datetime import datetime

# Read in the file
with open("logs/main.txt", "r") as infile:
    contents = infile.readlines()
contents = [c.strip() for c in contents]

# Grab the dates
dates = [line.split(" - ")[0].strip() for line in contents]
dates = [datetime.strptime(d, "%d-%m-%y %H:%M:%S") for d in dates]

# Zip contents and dates together
zipped = list(zip(contents, dates))
# Sort them
sorted_zipped = sorted(zipped, key = lambda x: x[1], reverse=True)
# Unzip them and grab the sorted contents
sorted_contents = next(zip(*sorted_zipped))

# Write the sorted contents back out
with open("outfile.txt", "w") as out:
    out.write("\n".join(sorted_contents))
