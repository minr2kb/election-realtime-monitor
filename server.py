from flask import Flask, render_template, request
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time
import datetime
from crawler import crawl_nec, crawl_vc

app = Flask(__name__)

@app.route('/') 
def root():
    return """<button onclick="window.location.assign('/VC20')">20대 선거 투표현황</button>"""


@app.route('/VC20') 
def vc20():
    now = str(datetime.datetime.now())
    return '<h3>Last update: '+now+'</h3>'+crawl_vc() 

# @app.route('/VC19') 
# def vc19():    
#     now = str(datetime.datetime.now())
#     return '<h3>Last update: '+now+'</h3>'+crawl_nec() 

if __name__ == '__main__':
    app.run(debug=True, port=5003)