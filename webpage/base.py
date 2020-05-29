from flask import Flask
from flask import Flask, session, redirect, url_for, request,render_template
import matplotlib.pyplot as plt
import subprocess
import pandas as pd

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='GET':
        return """

        <h1>Historico Graficador acciones</h1>
   
        
        <form action="/" method="post">
        <input type="date" id="start" name="start"
        value="2016-07-22"
        min="2015-01-01" max="2019-12-31">

        <input type="date" id="start" name="finish"
        value="2019-07-30"
        min="2015-01-01" max="2019-12-31">

        <label for="ticket">Ingrese la Accion</label><br>
        <input name="ticket" id="ticket" list="tickets">
        

        <br>
        
        <input formmethod="post" type="submit" value="Graficar">
        </form>
        
        <datalist id="tickets">
           <option>AAPL</option>
           <option>BTC-USD</option> 
           <option>GOOG</option> 
        </datalist>


        """
    if request.method=='POST':
        inicio = request.form['start']
        fin    = request.form['finish']
        ticket = request.form['ticket']
        print(ticket)
        subprocess.check_call("bash ../Informacion/script.sh '%s' '%s' '%s' > temp.csv " % (ticket,inicio,fin),   shell=True)

        df = pd.read_csv('temp.csv',sep=',')

        fig, ax = plt.subplots(figsize=(20,10))
        
        ax.plot(df['Date'],df['Close'])

        # naming the y-axis
        plt.ylabel('Close')
        # naming the x-axis
        plt.xlabel('Date')
        # plot title
        plt.title(ticket + " From %s to %s" % (inicio,fin) )
        ax.set_xticks(df['Date'][::10])       
        ax.locator_params(axis='x', nbins=10)
        plt.savefig('static/images/plot_9.png')
        return render_template('plot.html', url='/static/images/plot_9.png')

    
