from Scrapper import Scrapper
import re, json
from settings import *

class BruteForce(Scrapper):

    def __init__(self):
        self.alg = 'Brute Force'

    def splitKeyword(self, text):
        return text.lower().split(' ')

    def cleanKeyword(self, text):
        return re.sub('[^A-Za-z0-9-()]+', ' ', text.lower())

    def findIndex(self, data, key):
        for i in range(len(data)):
            if data[i] == key:
                return i
        return None
    
    def jsonSave(self, data, name):
        with open(BASE_PATH+'data/cache/{name}.json'.format(name=name), 'w+') as f:
            return json.dump(data, f, separators=(',', ':'), sort_keys=True)

    def cacheDict(self, text, data):
        dictKeyword = self.json_load(BASE_PATH+'data/cache/index.json')
        split = self.splitKeyword
        clean = self.cleanKeyword
        findIndex = self.findIndex
        text = split(text)
        result = []
        for key in text:
            if key not in dictKeyword:
                dictKeyword[key] = []
                for i in range(len(data)):
                    splitTitle = split(clean(data[i]['title']))
                    index = findIndex(splitTitle,key)
                    if index != None:
                        dictKeyword[key].append((i,index))
                        result.append(data[i])
        
        return [self.jsonSave(dictKeyword,'index'), result]

    def valueExists(self, data, value):

        for i, d in enumerate(data):
            if d['title'] == value:
                return True       
        return False

    def search(self, text):
        result = []
        data = self.json_load(BASE_PATH+'data/fix/data.json')
        dictKeyword = self.json_load(BASE_PATH+'data/cache/index.json')

        split = self.splitKeyword
        clean = self.cleanKeyword
        keyword = split(clean(text))
        for item in keyword:
            if item in dictKeyword:
                for i in dictKeyword[item]:
                    if not self.valueExists(result,data[i[0]]['title']):
                        result.append(data[i[0]])
                    
            else:
                [_,res] = self.cacheDict(text,data)
                for i in res:
                    if not self.valueExists(result,i['title']):
                        result.append(i) 
        return result


        
if __name__ == "__main__":

    bf = BruteForce()
    search = bf.search('the true')
    for i in search:
        print(i['title'])

                