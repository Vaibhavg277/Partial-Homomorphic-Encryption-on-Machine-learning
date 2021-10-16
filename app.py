import numpy as np
from flask import Flask, request, jsonify, render_template,redirect,url_for
import json
from cust import *
from servercalc import *
from os import path

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])

def home():
    
    return render_template('index.html')

@app.route('/customerEncryption',methods=['GET','POST'])
def customerEncryption():
    if not path.exists('custkeys.json'):
        storeKeys()
        
    pub_key, priv_key = getKeys()
    
    features = [int(x) for x in request.form.values()]
    datafileCustomer=serializeDataCustomer(pub_key,features)
    with open('data.json', 'w') as file: 
        json.dump(datafileCustomer, file)
    
    keys=[pub_key,priv_key]
    return render_template('cust.html',keys=keys)

@app.route('/company',methods=['GET','POST'])
def company():
    datafileCompany=serializeDataCompany()
    with open('answer.json', 'w') as file:
        json.dump(datafileCompany,file)
		
        
    return render_template('company.html',datafileCompany=datafileCompany)
   
    #return redirect(url_for('result'))

@app.route('/result',methods=['GET','POST'])
def result():
    answer_file=loadAnswer()
    answer_key=paillier.PaillierPublicKey(n=int(answer_file['pubkey']['n']))
    answer = paillier.EncryptedNumber(answer_key, int(answer_file['values'][0]), int(answer_file['values'][1]))
    pub_key, priv_key = getKeys()
    if (answer_key==pub_key):
        final_result=priv_key.decrypt(answer)
 	
    
    return render_template('result.html',final_result=final_result)

    
if __name__ == "__main__":
    app.run(debug=True)