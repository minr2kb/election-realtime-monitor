from flask import Flask, render_template, request
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time
from crawler import crawl_nec 

app = Flask(__name__)

@app.route('/') 
def root():    
    return crawl_nec()

if __name__ == '__main__':
    app.run(debug=True, port=5003)