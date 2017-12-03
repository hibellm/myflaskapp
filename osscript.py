from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import os
import logging
import time
import subprocess

logging.basicConfig(level=logging.DEBUG)
app =Flask(__name__)

command1="shell1.sh"
command2="shellx.sh"
command3="shell3.sh"
command4="shell4.sh"
# THE INITIAL PAGE
# Index 
@app.route('/shell', methods=['GET','POST'])

def shell(): 
    if request.method == 'POST':
        if request.form['runscript'] == 'runvendor':
            #os.system(command1)
            a=os.popen(command1).read()
            #__file__="listfiles1.txt"
            #print('File         :', __file__)
            #print('Access time  :', time.ctime(os.path.getatime(__file__)))
            #print('Modified time:', time.ctime(os.path.getmtime(__file__)))
            #print('Change time  :', time.ctime(os.path.getctime(__file__)))
            #print('Size         :', os.path.getsize(__file__))            
            flash('Updated meta data RWD_META_MDH.VendorDetails','success')                        
            return redirect(url_for('shell'))           
        elif request.form['runscript'] == 'rundata':
            #os.system(command2)
            a=os.popen(command2).read()
 
            try:
                 subprocess.call([command2])
            except OSError:
                 print ('wrongcommand does not exist')
                 flash('nooooooo RWD_META_MDH.DSDetails','danger')
            flash('Updated meta data RWD_META_MDH.DSDetails','success')
            return redirect(url_for('shell'))           
        else:
            os.system(command3)
            return redirect(url_for('shell'))
    elif request.method == 'GET':
        return render_template('shell.html')
        
    
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug = True)

