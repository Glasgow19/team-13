import os
import json

# database written in java even though app written in Java
def recommend():
    java_cmd = 'java -classpath sqlite-jdbc.jar:javax.json-1.0.jar:. dbServer '

    create = java_cmd + 'create hello'
    new_account = java_cmd + 'newAccount {"clientID": "goodbye"}'
    search = java_cmd + 'search ABCDEFGH,90'

    os.system(create)
    os.system(search)

    recommendations = []

    with open('../database/output.txt') as f:
        recos = f.readline().split(',')
        for r in recos:
            recommendations.append(r)

    f.close()
    return recommendations


if __name__ == "__main__":
    recommend()
