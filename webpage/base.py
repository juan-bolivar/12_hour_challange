from flask import Flask
from flask import Flask, session, redirect, url_for, request,render_template
import matplotlib.pyplot as plt
import subprocess
import pandas as pd
from random import randint
import os
import glob


app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='GET':
        return render_template('base.html')
    
   
    if request.method=='POST':

       
        files = glob.glob('static/images/*')

        for f in files:
            os.remove(f)
        
        inicio = request.form['start']
        fin    = request.form['finish']
        ticket = request.form['ticket']
        subprocess.check_call("bash ../Informacion/script.sh '%s' '%s' '%s' > temp.csv " % (ticket,inicio,fin),   shell=True)

        df = pd.read_csv('temp.csv',sep=',')
        fig, ax = plt.subplots(figsize=(20,10))
        ax.plot(df['Date'],df['Close'])
        plt.ylabel('Close')
        plt.xlabel('Date')
        plt.title(ticket + " From %s to %s" % (inicio,fin) )
        ax.set_xticks(df['Date'][::10])       
        ax.locator_params(axis='x', nbins=10)
        rand = randint(0,100000)
        plt.savefig('static/images/plot_' + str(rand) + '.png')
        return render_template('plot.html', url='static/images/plot_'+ str(rand) +'.png')

    
