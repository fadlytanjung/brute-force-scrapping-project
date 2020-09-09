from flask import Flask, jsonify ,request, render_template
from fuzzywuzzy import fuzz
from BruteForce import BruteForce
import sys, os
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))
from settings import *

bf = BruteForce()
app = Flask(__name__)
static = BASE_PATH+'static/'

@app.route('/')
def home():
    path = request.path
    return render_template('home.html', data=path)

@app.route('/search', methods=['POST'])
def search():

    start_time = time.time()
    jsonData = request.json
    search = bf.search

    data = search(jsonData['data'])
    newData = []
    for item in data:
        print(get_ratio(jsonData['data'],item['title']))
        if get_ratio(jsonData['data'],item['title']) > 50:
            newData.append(item)
    return jsonify({ 'code':200, 'message' : 'Data Fetched',
    'data': newData,'time':(time.time() - start_time) }), 200

def get_ratio(str1,str2):
    str1 = str1.lower()
    str2 = str2.lower()
    return fuzz.token_set_ratio(str1, str2)

@app.route('/crawl')
def crawl():
    path = request.path
    data = bf.json_load(static+'data.json')
    return render_template('crawl.html', data=path, dataTables=data)

@app.route('/crawlprocess', methods=['POST'])
def crawlprocess():
    jsonData = request.json
    bf.ruangmahasiswaHelper()
    bf.eventkampusHelper()
    bf.anakteknikHelper()
    bf.informasilombaHelper()
    bf.lombapadHelper()
    # scr.lombaasiaHelper() # suspend
    bf.infolombaHelper()
    bf.eventMahasiswa()
    bf.jadwalEvent()
    bf.eventpelajarHelper()
    bf.mergeJsonFiles('data/')

    try:
        return jsonify({ 'code':200, 'message' : 'Success' }), 200
    except e:
        return jsonify({ 'code':500, 'message' : 'Success', 'error': str(e) }), 500
    

        
if __name__ == "__main__":
    # app.run(debug=True, port=8080)
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)