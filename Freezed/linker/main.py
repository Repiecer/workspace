from flask import Flask, request, template_rendered
import json
from time import sleep
app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def accept():
    if request.method == 'POST':
        addtt = False
        resultjs = json.loads(str(request.data, encoding='utf-8'))
        with open('result.json', 'r') as f:
            textjs = json.loads(f.read())
            if len(textjs) != 0:
                for i in range(len(textjs)):
                    if resultjs["name"] == textjs[i]["name"]:
                        with open('result.json', 'w') as a:
                            textjs[i]["location"] = resultjs["location"]
                            a.write(json.dumps(textjs))
                            addtt = False
                        break
                    else:
                        
                        addtt = True
            else:
                textjs.append(resultjs)
                with open('result.json', 'w') as a:
                    a.write(json.dumps(textjs))
                    addtt = False
            if addtt:
                
                textjs.append(resultjs)
                with open('result.json', 'w') as a:
                    a.write(json.dumps(textjs))
                    addtt = False
        with open('result.json', 'r') as t:
            return t.read()
    elif request.method == "GET":
        with open('result.json', 'r') as t:
            return t.read()
    

if __name__ == '__main__':
    app.run(port=25560, debug=True)