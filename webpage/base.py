from   random            import randint
from   flask             import Flask, session, redirect, url_for, request,render_template
from   bokeh.embed       import components
from   bokeh.plotting    import figure
from   bokeh.resources   import INLINE
import matplotlib.pyplot as plt
import pandas            as pd
import subprocess
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
        df['Date'] = pd.to_datetime(df['Date'])

        
        p = figure(plot_width = 500 , plot_height=500 ,x_axis_type="datetime")

        p.line(df['Date'],df['Close'],line_width=2)

        js_resources  = INLINE.render_js()
        css_resources = INLINE.render_css()
        
        script , div = components(p)

        return render_template('plot.html', script=script , div=div ,js_r=js_resources , css_r=css_resources)

    
