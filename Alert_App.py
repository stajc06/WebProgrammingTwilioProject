from flask import Flask
app = Flask(__name__)

@app.route('/get')
def get():
    #error check
    results=[]

    #add first 10 reminders in database to results


    return results

#@app.route('/set')
#def set(time, text):
    #error check/formatting check

    #add reminder

    #nothing to return


#@app.route('/drop')
#def drop():
    #are we dropping all reminders or just one??