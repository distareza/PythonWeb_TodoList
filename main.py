from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
import myconfiguration
from Data import Data

app = Flask(__name__)
app.config['SECRET_KEY'] = myconfiguration.secret_key

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    data = Data()
    return jsonify(data.getAllData())

@app.route("/master-data")
def masterdata():
    data = Data()
    return jsonify(data.getAllMasterData())

@app.route("/detail-data/<int:todo_id>")
def detaildata(todo_id):
    data = Data()
    return jsonify(data.getListData(todo_id))

@app.route("/update-data", methods=['POST'])
def updatedata():
    try:
        id = int(request.form.get("id"))
        complete = bool(request.form.get("complete") == "true")
        Data().updateDetail(id, complete)
        return { "response": "OK" }, 200
    except Exception as e:
        return { "response" : "ERROR", "message" : e}, 400

@app.route("/save-data", methods=['POST'])
def adddata():
    try:
        todo_name = request.form.get("todo-name")
        todo_desc = request.form.get("message-text")
        tasks = request.form.getlist("task")

        data = Data()
        data.addMasterData(todo_name, todo_desc)
        for task in tasks:
            data.addDetailData(todo_name, task)

        return {"response": "OK"}, 200
    except Exception as e:
        return { "response" : "ERROR", "message" : e}, 400

@app.route("/remove-data", methods=['POST'])
def removedata():
    try:
        todo_name = request.form.get("todo-name")
        data = Data()
        data.removeMasterData(todo_name)
        return {"response": "OK"}, 200
    except Exception as e:
        return { "response" : "ERROR", "message" : e}, 400

if __name__ == '__main__':
    app.run(debug=True)