# testing database file

import os

java_cmd = 'java -classpath sqlite-jdbc.jar:javax.json-1.0.jar:. dbServer '

create = java_cmd + 'create hello'
new_account = java_cmd + 'newAccount {"clientID": "goodbye"}'
search = java_cmd + 'search ABCDEFGH,80'

#s.system(create)
#os.system(new_account)

os.system(search)

import json

with open('output.txt') as f:
    for line in f:
        temp = json.loads(line)
        print(temp['suggestions'][0])

f.close()

