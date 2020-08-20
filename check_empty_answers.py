import json
import sys

with open(sys.argv[1]) as fp:
    d = json.load(fp)

x = y = 0

for item in d['data']: 
   for para in item['paragraphs']: 
       for qas in para['qas']: 
           if len(qas['answers']) <= 0 and qas['is_impossible'] == False: 
               print(qas) 
               x += 1 
           elif qas['is_impossible'] == False: 
               y += 1

print("%d empty, %d OK" % (x, y))

