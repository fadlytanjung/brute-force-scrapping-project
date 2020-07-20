from bs4 import BeautifulSoup as soup
import requests as req
import numpy as np
import sys, os
import json, glob
import time
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
        for i in range(1,500): #500
            print('eventpelajar page '+str(i))
            URL = 'https://eventpelajar.com/lomba/page/'+str(i)
            page = self.reqPage(URL)
            if page.status_code == 200:
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
        
                    category = item.find_all('span', class_='ct-meta-element')
                    if len(category) > 0:
                        category = category[0].get_text().strip()
                    location  = ''
                    
                    description = item.find_all('div', class_='entry-excerpt')[0].get_text().strip()
                    date = item.find_all('li', class_='ct-meta-date')
                    if len(date)> 0:
                        date = date[0].get_text().strip()
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
        while i <=960: #960
            print('ruang mahasiswa page '+str(i))
            page = self.reqPage(BASE_URL+str(i))
            if page.status_code != 404:
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
        while i <=900: #900
            print('event kampus page '+str(i))
            page = self.reqPage(BASE_URL+str(i))
            if page.status_code != 404:
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

    def anakteknikHelper(self):
        BASE_URL = [
        'https://www.anakteknik.co.id/api/event/paginate?last=2020-04-19T02:42:43.796Z&category=1',
        'https://www.anakteknik.co.id/api/event/paginate?last=2019-06-19T02:42:43.796Z&category=1',
        'https://www.anakteknik.co.id/api/event/paginate?last=2019-03-28T16:06:01.252Z&category=1',
        'https://www.anakteknik.co.id/api/event/paginate?last=2018-12-30T03:37:12.471Z&category=1',
        'https://www.anakteknik.co.id/api/event/paginate?last=2018-10-10T07:58:10.712Z&category=1',
        'https://www.anakteknik.co.id/api/event/paginate?last=2018-08-31T15:42:14.940Z&category=1',
        'https://www.anakteknik.co.id/api/event/paginate?last=2018-07-03T04:56:59.494Z&category=1',
        'https://www.anakteknik.co.id/api/event/paginate?last=2018-04-18T00:45:39.844Z&category=1']

        temp = []
        for linkURL in BASE_URL:

            print('anak teknik page '+linkURL)
            page = self.reqPage(linkURL).json()

            pageData = page['data']
            for item in pageData:
                title = item['judul']

                link = 'https://www.anakteknik.co.id/e/'+item['slug']
                image = 'https://www.anakteknik.co.id/img/bhrearka/event/'+item['_id']+'/thumb/'+item['thumbPoster']
                category = ''   
                location  = item['lokasi']
                description = item['sinopsis']
                date = item['tanggal_event']
                
                newObject = {
                    'title': title,
                    'link': link,
                    'image': image,
                    'category': category,
                    'location': location,
                    'description': description,
                    'date': date,
                    'source':'https://www.anakteknik.co.id/'
                }
                temp.append(newObject)

        return self.json_save(temp, 'anakteknik')

    def informasilombaHelper(self):
        BASE_URL = [
        'https://www.informasilomba.com/search?updated-max=2020-04-10T07%3A39%3A00-07%3A00&max-results=25#PageNo=1',
        'https://www.informasilomba.com/search?updated-max=2020-02-10T07%3A39%3A00-07%3A00&max-results=25#PageNo=1',
        'https://www.informasilomba.com/search?updated-max=2019-12-10T07%3A39%3A00-07%3A00&max-results=25#PageNo=1',
        'https://www.informasilomba.com/search?updated-max=2019-10-10T07%3A39%3A00-07%3A00&max-results=25#PageNo=1',
        'https://www.informasilomba.com/search?updated-max=2019-08-10T07%3A39%3A00-07%3A00&max-results=25#PageNo=1'
        ]

        temp = []
        
        for i in BASE_URL:
            print('informasi lomba page '+str(i))
            page = self.reqPage(i)
            parser = self.htmlParser(page.content)
            tag = parser.find_all('article', class_='post')
            for item in tag:
                title = item.find_all('h2', class_='post-title')[0]
                if title != None:
                    title = title.get_text().strip().encode('ascii', 'ignore')
                link = item.find_all('h2', class_='post-title')[0].find_all('a',href=True)[0]['href']
                srcImg = item.find_all('meta')
                image = srcImg[0].get('content') if len(srcImg) > 0 else srcImg
                category = item.find_all('span', class_='label-info')[0]
                if category.i != None:
                    category.i.decompose()
                category = category.get_text().strip()
                location  = ''
                description = item.find_all('div', class_='post-body')[0].get_text().strip()
                date = ''
            
                newObject = {
                    'title': str(title.decode('utf-8')),
                    'link': link,
                    'image': image,
                    'category': category,
                    'location': location,
                    'description': description,
                    'date': date,
                    'source':'https://www.informasilomba.com/'
                }
                temp.append(newObject)
        return self.json_save(temp, 'informasilomba')

    def lombapadHelper(self):
        BASE_URL = 'https://lombapad.com/page/'

        temp = []
        i = 1
        while i <=160: #160
            print('lombapad page '+str(i))
            page = self.reqPage(BASE_URL+str(i))
            if page.status_code != 404:
                parser = self.htmlParser(page.content)
                tag = parser.find_all('article', class_='item-content')
                for item in tag:
                    title = item.find_all('h2', class_='entry-title')[0]
                    if title != None:
                        title = title.get_text().strip().encode('ascii', 'ignore')

                    link = item.find_all('h2', class_='entry-title')[0].find_all('a',href=True)[0]['href']
                    srcImg = item.find_all('img',src=True)
                    image = srcImg[0]['src'] if len(srcImg) > 0 else srcImg
                    category = item.find_all('span', class_='cat-links-content')[0].get_text().strip()
                    location  = ''
                    description = item.find_all('div', class_='entry-content')[0].get_text().strip()
                    date = item.find_all('time', class_='entry-date')[0].get_text().strip()
                    
                    newObject = {
                        'title': str(title.decode('utf-8')),
                        'link': link,
                        'image': image,
                        'category': category,
                        'location': location,
                        'description': description,
                        'date': date,
                        'source':'https://lombapad.com/'
                    }
                    temp.append(newObject)
            i+=1
        
        return self.json_save(temp, 'lombapad')

    def lombaasiaHelper(self):
        BASE_URL = 'http://lomba.asia/?page=1'

        temp = []
        i = 1
        while i <=500: #500
            time.sleep(1)
            print('lombaasia page '+str(i))
            page = self.reqPage(BASE_URL+str(i))
            if page.status_code != 404:
                parser = self.htmlParser(page.content)
                tag = parser.find_all('article', class_='card')
                for item in tag:
                    title = item.find_all('h2', class_='card-title')[0]
                    if title != None:
                        title = title.get_text().strip().encode('ascii', 'ignore')

                    link = item.find_all('h2', class_='card-title')[0].find_all('a',href=True)[0]['href']
                    srcImg = item.find_all('img',class_='card-img-top',src=True)
                    image = srcImg[0]['src'] if len(srcImg) > 0 else srcImg
                
                    category = item.find_all('nav', class_='border-top')[0].get_text().strip()
                    location  = ''
                    description = item.find_all('p', class_='card-text')[0].get_text().strip()
                    date = item.find_all('small')[0]
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
                        'source':'http://lomba.asia/'
                    }
                    temp.append(newObject)
            i+=1
        
        return self.json_save(temp, 'lombaasia')

    def infolombaHelper(self):
        BASE_URL=[
        'http://www.info-lomba.com/?max-results=5',
        'http://www.info-lomba.com/search?updated-max=2018-11-10T08%3A06%3A00%2B07%3A00&amp;max-results=5',
        'http://www.info-lomba.com/search?updated-max=2018-10-27T13%3A34%3A00%2B07%3A00&amp;max-results=5',
        'http://www.info-lomba.com/search?updated-max=2018-10-23T16%3A55%3A00%2B07%3A00&amp;max-results=5',
        'http://www.info-lomba.com/search?updated-max=2018-10-14T17%3A21%3A00%2B07%3A00&amp;max-results=5',
        'http://www.info-lomba.com/search?updated-max=2018-03-05T10%3A49%3A00%2B07%3A00&amp;max-results=5',
        'http://www.info-lomba.com/search?updated-max=2018-01-27T11%3A00%3A00%2B07%3A00&amp;max-results=5',
        'http://www.info-lomba.com/search?updated-max=2018-01-23T19%3A56%3A00%2B07%3A00&amp;max-results=5',
        'http://www.info-lomba.com/search?updated-max=2018-01-21T16%3A36%3A00%2B07%3A00&amp;max-results=5',
        'http://www.info-lomba.com/search?updated-max=2018-11-10T08%3A06%3A00%2B07%3A00&amp;max-results=5',
        'http://www.info-lomba.com/search?updated-max=2017-08-29T06%3A34%3A00%2B07%3A00&amp;max-results=5']

        temp = []
        
        for i in BASE_URL:
            print('info lomba page '+str(i))
            page = self.reqPage(i)
            parser = self.htmlParser(page.content)
            tag = parser.find_all('article', class_='post')
            for item in tag:
                title = item.find_all('h2', class_='post-title')[0]
                if title != None:
                    title = title.get_text().strip().encode('ascii', 'ignore')
                link = item.find_all('h2', class_='post-title')[0].find_all('a',href=True)[0]['href']
                srcImg = item.find_all('meta')
                image = srcImg[0].get('content') if len(srcImg) > 0 else srcImg
                categoryTemp = item.find_all('span', class_='label-info')
                category = categoryTemp[0] if len(categoryTemp) > 0 else None

                if category is not None:
                    if category.i != None:
                        category.i.decompose()
                    category = category.get_text().strip()
                else:
                    category =''
                location  = ''
                description = item.find_all('div', class_='post-body')[0].get_text().strip()
                date = ''
            
                newObject = {
                    'title': str(title.decode('utf-8')),
                    'link': link,
                    'image': image,
                    'category': category,
                    'location': location,
                    'description': description,
                    'date': date,
                    'source':'http://www.info-lomba.com/'
                }
                temp.append(newObject)
        return self.json_save(temp, 'infolomba')

if __name__ == "__main__":
    
    scr = Scrapper()
    scr.eventpelajarHelper()
    scr.ruangmahasiswaHelper()
    scr.eventkampusHelper()
    scr.anakteknikHelper()
    scr.informasilombaHelper()
    scr.lombapadHelper()
    scr.lombaasiaHelper()
    scr.infolombaHelper()
    scr.mergeJsonFiles(BASE_PATH+'data/')
 
    
