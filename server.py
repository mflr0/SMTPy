##
##  server.py
##  SNMPy
##
##  Created by Hilden13 on 26/05/2024.
##  Contributor(s): Hilden13
##

import json
from flask import Flask, jsonify
import os.path

app = Flask(__name__)

savefile: dict = {}
SAVENAME = "savedata.json"
SENTMAILS = "sent.json"

@app.route('/smtpy/<string:user>/<int:id>', methods=['GET'])
def register_phish(user: str, id: int):
    if os.path.isfile(SENTMAILS) is False:
        return '', 500
    sent_file = open(SENTMAILS, "r")
    sent_text = sent_file.read()

    if sent_text.find(user) == -1 or sent_text.find(str(id)) == -1 or id > 2147483647 or id < 1000000000 or json.dumps(savefile).find(str(id)) != -1:
        return '', 400
    sent_file.close()

    if savefile.keys().__contains__(user) is False:
        savefile[user] = [id]
    else:
        cur_list: list = savefile[user]
        cur_list.append(id)
        savefile[user] = cur_list
    
    saving_file = open(SAVENAME, "w")
    saving_file.write(json.dumps(savefile))
    saving_file.close()
    return '', 200

def load_save():
    if os.path.isfile(SAVENAME) is False:
        open_file = open(SAVENAME, "w")
        open_file.write("{}")
        open_file.close()
    open_file = open(SAVENAME, "r")
    if open_file is False:
        return False
    savefile: dict = json.loads(open_file.read())
    open_file.close()
    return True

if __name__ == '__main__':
    if load_save():
        print(savefile)
        app.run(host='0.0.0.0', port=9900)