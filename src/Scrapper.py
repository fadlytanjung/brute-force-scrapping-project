from bs4 import BeautifulSoup as soup
import requests as req
import numpy as np
import sys, os
import json, glob
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))
from settings import *

class Scrapper:
    def __init__(self):
        self.data = []

    def reqPage(self, URL):
        return req.get(URL)
    
    def htmlParser(self, content):
        return soup(content, 'html.parser')
    
    def json_save(self, data, name):
        with open(BASE_PATH+'data/{name}.json'.format(name=name), 'w+') as f:
            return json.dump(data, f)
    
    def json_load(self, path):
        with open(path, 'r') as f:
            return json.load(f)
    def mergeJsonFiles(self, path):

        result = []
        for item in glob.glob(BASE_PATH+'{path}*.json'.format(path=path)):
            with open(item, 'rb') as f:
                data = json.load(f)
                result.append(data)
            print(item, len(data))
        print(len(result))
        result = np.hstack(result).tolist()
        print('after merge: ', len(result))
        with open(BASE_PATH+'{path}fix/data.json'.format(path=path), 'w') as outfile:
            json.dump(result, outfile, separators=(',', ':'), sort_keys=True, indent=4)
        with open(BASE_PATH+'static/data.json', 'w') as outfile:
            json.dump(result, outfile, separators=(',', ':'), sort_keys=True, indent=4)
        return 'Successfull'

    def eventpelajarHelper(self):
        BASE_URL = 'https://eventpelajar.com/lomba/page/'
        temp = []
        for i in range(1,48):
            print('eventpelajar page '+str(i))
            URL = 'https://eventpelajar.com/lomba/page/'+str(i)
            page = self.reqPage(URL)
            parser = self.htmlParser(page.content)
            
            tag = parser.find_all('article', class_='entry-card')
            
            for item in tag:
                title = item.find_all('h2', class_='entry-title')[0]
                if title.span != None:
                    title.span.decompose()
                
                title = title.get_text().strip()
                link = item.find_all('h2', class_='entry-title')[0].find_all('a',href=True)[0]['href']
                
                srcImg = item.find_all('a', class_='ct-image-container')
                image = srcImg[0].find_all('img', src=True)[0]['src'] if len(srcImg) > 0 else srcImg
                
                category = item.find_all('span', class_='ct-meta-element')[0].get_text().strip()
                location  = ''
                
                description = item.find_all('div', class_='entry-excerpt')[0].get_text().strip()
                date = item.find_all('li', class_='ct-meta-date')[0].get_text().strip()
            
                newObject = {
                    'title': title,
                    'link': link,
                    'image': image,
                    'category': category,
                    'location': location,
                    'description': description,
                    'date': date,
                    'source':'https://eventpelajar.com/lomba/'
                }
                temp.append(newObject)
        return self.json_save(temp, 'eventpelajar')

    def ruangmahasiswaHelper(self):
        BASE_URL = 'https://event.ruangmahasiswa.com/event/list/'

        temp = []
        i = 1
        while i <=192:
            print('ruang mahasiswa page '+str(i))
            page = self.reqPage(BASE_URL+str(i))
            parser = self.htmlParser(page.content)
            tag = parser.find_all('div', class_='card')
            for item in tag:
                title = item.find_all('p', class_='title')[0]
                if title != None:
                    title = title.get_text().strip().encode('ascii', 'ignore')

                link = item.find_all('p', class_='title')[0].find_all('a',href=True)[0]['href']
                srcImg = item.find_all('figure', class_='image')
                image = srcImg[0].find_all('img', src=True)[0]['src'] if len(srcImg) > 0 else srcImg
                category = item.find_all('p', class_='subtitle')[0].get_text().strip()
                location  = item.find_all('tr', class_='location')[0].find_all('td')[1].get_text().strip()
                description = ''
                date = item.find_all('tr', class_='time')[0].find_all('td')[1].get_text().strip()
            
                newObject = {
                    'title': str(title.decode('utf-8')),
                    'link': link,
                    'image': image,
                    'category': category,
                    'location': location,
                    'description': description,
                    'date': date,
                    'source':'https://event.ruangmahasiswa.com/'
                }
                temp.append(newObject)
            i = i+5 if i == 1 else i+6
        
        return self.json_save(temp, 'ruangmahasiswa')
    
    def eventkampusHelper(self):
        BASE_URL = 'https://eventkampus.com/event/kategori/expo?page='

        temp = []
        i = 1
        while i <=9:
            print('event kampus page '+str(i))
            page = self.reqPage(BASE_URL+str(i))
            parser = self.htmlParser(page.content)
            tag = parser.find_all('div', class_='cd-beasiswa')
            for item in tag:
                title = item.find_all('div', class_='cd-beasiswa__judul')[0]
                if title != None:
                    title = title.get_text().strip().encode('ascii', 'ignore')

                link = item.find_all('div', class_='cd-beasiswa__judul')[0].find_all('a',href=True)[0]['href']
                srcImg = item.find_all('div', class_='cd-beasiswa__foto')
                image = srcImg[0].select('img', src=True)[0]['data-src'] if len(srcImg) > 0 else srcImg
                category = item.find_all('div', class_='cd-beasiswa__sub')[0].a

                if category.i != None:
                    category.i.decompose()
                category = category.get_text().strip()
                location  = item.find_all('div', class_='cd-beasiswa__sub')[0].find_all('div', class_='cd-beasiswa__place')[0]
                if location.i != None:
                    location.i.decompose()
                location = location.get_text().strip()
                description = ''
                date = item.find_all('div', class_='cd-beasiswa__sub')[0].find_all('div', class_='mb-2')[1]
                if date.i != None:
                    date.i.decompose()
                date = date.get_text().strip()
            
                newObject = {
                    'title': str(title.decode('utf-8')),
                    'link': link,
                    'image': image,
                    'category': category,
                    'location': location,
                    'description': description,
                    'date': date,
                    'source':'https://eventkampus.com/event/kategori/expo'
                }
                temp.append(newObject)
            i+=1
        return self.json_save(temp, 'eventkampus')

if __name__ == "__main__":
    
    scr = Scrapper()
    scr.eventpelajarHelper()
    scr.ruangmahasiswaHelper()
    scr.eventkampusHelper()
    scr.mergeJsonFiles(BASE_PATH+'data/')
 
    
