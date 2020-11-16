from flask import Flask,render_template,request
import json
app= Flask(__name__)
@app.route('/')
def my_form():
    return render_template('firstpage_2.html')
@app.route('/data',methods=['GET'])
def send_data():
    data = json.dumps([8,2,4,2,8])
    labels = json.dumps(["Work","Eat","TV","GYM","Sleep"])
    return render_template("testing_for_js.html", data=data,
                           labels=labels)

if __name__=="__main__":
        app.run(debug=True)