import xml.etree.ElementTree as ET;
import os;
import pandas as pd; #데이터관리
from pandas import DataFrame,Series; # 데이터 관리

from flask import Flask,g,jsonify;
from flask_cors import CORS;
from flask import request;
app = Flask(__name__);
CORS(app);
    
@app.route("/list")
def test():
    cPath = os.getcwd()
    fname = "lmsCalendar/schedule.xml"
    tree = ET.parse(cPath+"/"+fname)
    schedules = tree.getroot()
    #<color>#154790</color><textColor>white</textColor>
    rows = []
    for schedule in schedules:
        title = schedule.find("title").text
        start = schedule.find("start").text
        end = schedule.find("end").text
        status = schedule.find("status").text
        id = schedule.get("id")
        color = "#154790"
        textColor = "white"
        rows.append({"title":title, "start":start ,"end":end ,"color":color, "textColor":textColor,"status":status ,"pyid":id})
    
    df = DataFrame(rows)
    json_data = df.to_json(orient='records')
    return json_data

@app.route("/write")
def write():
    start = request.args.get('startdate', default = '0', type = str);
    end = request.args.get('enddate', default = '0', type = str);
    title = request.args.get('title', default = '0', type = str);
    
    cPath = os.getcwd()
    fname = "lmsCalendar/schedule.xml"
    tree = ET.parse(cPath+"/"+fname)
    root = tree.getroot()
    id = int(root[len(root)-1].get("id"))+1
    
    add_el = ET.Element("schedule")
    add_el.set("id",str(id))
    
    e_title = ET.SubElement(add_el, "title")
    e_title.text = title
    e_start = ET.SubElement(add_el, "start")
    e_start.text = start
    e_end = ET.SubElement(add_el, "end")
    e_end.text = end
    e_color = ET.SubElement(add_el,"color")
    e_color.text = "#154790"
    e_textColor = ET.SubElement(add_el,"textColor")
    e_textColor.text = "white"
    e_status = ET.SubElement(add_el,"status")
    e_status.text ="0"
    
    root.append(add_el)
    tree.write(cPath+"/"+fname)
    return ""
@app.route("/update")
def update():
    start = request.args.get('startdate', default = '0', type = str);
    end = request.args.get('enddate', default = '0', type = str);
    title = request.args.get('title', default = '0', type = str);
    id = request.args.get('id', default = '0', type = str);
    #print(title+"/"+start+"/"+end)
    #row = {"title":title, "start":start ,"end":end ,"color":"#154790", "textColor":"white","status":"1"}
    
    cPath = os.getcwd()
    fname = "lmsCalendar/schedule.xml"
    tree = ET.parse(cPath+"/"+fname)
    root = tree.getroot()

    
    # 요소를 수정합니다.
    for schedule in root.findall("schedule"):
        if schedule.get("id") == id:
            e_title = schedule.find("title")
            e_title.text = title
            e_start = schedule.find("start")
            e_start.text = start
            e_end = schedule.find("end")
            e_end.text = end
            
    tree.write(cPath+"/"+fname)
    return ""
@app.route("/del")
def delddd():
    id = request.args.get('id', default = '0', type = str);
    #print(title+"/"+start+"/"+end)
    #row = {"title":title, "start":start ,"end":end ,"color":"#154790", "textColor":"white","status":"1"}
    
    cPath = os.getcwd()
    fname = "lmsCalendar/schedule.xml"
    tree = ET.parse(cPath+"/"+fname)
    root = tree.getroot()

    
    # 요소를 수정합니다.
    for schedule in root.findall("schedule"):
        if schedule.get("id") == id:
            e_status = schedule.find("status")
            e_status.text = "1"
            
    tree.write(cPath+"/"+fname)
    return ""