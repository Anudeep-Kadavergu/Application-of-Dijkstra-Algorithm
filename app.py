from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd
import folium
import numpy as np
import geopy.distance

data=[]

json_data = {}
with open('data.json') as json_file: 
        json_data = json.load(json_file)
    
existing_loc =  json_data['existing_location']
existing_dist =  json_data['existing_distance']
loc = json_data["location"]
distance_json = json_data["distance"]

link = "https://www.google.com/search?q=longitude of "

for i in range(int(input("enter number of place you want:-"))):
    b=[]
    k=input("enter {} places:-".format(i+1))
    
    if k in existing_loc:
        print('json data')
        b.append(k)
        b.extend(json_data['location'][k])
    else:
        #extracting latitudes and longitudes from google using bs4
        try:
            b.append(k)
            page=requests.get(link+k)
            soup =BeautifulSoup(page.content,'html.parser')
            f=str(soup.find("div",{"class":"BNeawe iBp4i AP7Wnd"}).get_text())
            f=f.replace('° N','')
            f=f.replace('° E','')
            b.extend([float(x) for x in f.split(',')])
            #updating json file
            existing_loc.append(k)
            loc.update({k:[float(x) for x in f.split(',')]})
        except Exception as e:
            print("error is",e)
    data.append(b)

json_file.close()


import pandas as pd
import folium
import numpy as np

df=pd.DataFrame(data)
df.columns=["place","long","lati"]
coords_1 = (df["long"][0], df["lati"][0])
a=df.iloc[0,1]
b=df.iloc[0,2]
l1=list(df.loc[0,["long","lati"]])

folium_map = folium.Map(location=l1,zoom_start=10)

import geopy.distance
dist=[0]

source=input("enter the source or starting location:-")

for a in zip(df['long'],df['lati'],df['place']):
    str1 = "City: <b>"+str(a[2]).capitalize()+"</b><br/>"
    for b in zip(df['long'],df['lati'],df['place']): 
        if str(b[2]) != str(a[2]) :
            c = (b[0], b[1])
            if a[2]+"-"+b[2] in existing_dist :
                print("json data")
                str1 = str1+str(a[2]).capitalize()+' To '+str(b[2]).capitalize()+" : "+str(distance_json[a[2]+"-"+b[2]])+" km<br/>"
            elif b[2]+"-"+a[2] in existing_dist :
                str1 = str1+str(a[2]).capitalize()+' To '+str(b[2]).capitalize()+" : "+str(distance_json[b[2]+"-"+a[2]])+" km<br/>"
            else :
                g = geopy.distance.distance((a[0],a[1]), c).km 
                str1 = str1+str(a[2]).capitalize()+' To '+str(b[2]).capitalize()+" : "+str(int(g))+" km<br/>"
                existing_dist.append(a[2]+"-"+b[2])
                distance_json.update({a[2]+"-"+b[2]:int(g)})
           
    dist.append(geopy.distance.distance(coords_1, (a[0],a[1])).km )  
    popup1 = folium.Popup(str1, max_width=300,min_width=200,show=True) 
    if source == a[2]:
        folium.Marker(location=[a[0],a[1]],popup = popup1,icon=folium.Icon(color='red')).add_to(folium_map)
    else:
        folium.Marker(location=[a[0],a[1]],popup = popup1).add_to(folium_map)


distance=[]
dict_p={}
i=0
for a in df['place']:
    dict_p[a]=i
    i+=1

for a in df['place']:
    sub_distance=[]
    for b in df['place']:
        # URL = 'http://google.com/search?q=distance from '+a+' to '+b
        # content = requests.get(URL)
        # soup = BeautifulSoup(content.text, 'html.parser')
        # contentTable  =soup.find('div',{"class": "BNeawe deIvCb AP7Wnd"})
        # z=re.findall("\((.+)\)",contentTable.get_text())
        # if(len(z)!=0):
        #     k=z[0].split()[0]
        # else:
        #     k=0
        if str(a)+"-"+str(b) in existing_dist:
            sub_distance.append(distance_json[str(a)+"-"+str(b)])
        elif str(b)+"-"+str(a) in existing_dist:
            sub_distance.append(distance_json[str(b)+"-"+str(a)])
        else:
            sub_distance.append(0.0)       
    distance.append(sub_distance)


with open('data.json','w') as f: 
    json.dump(json_data, f, indent=4)    
f.close()

a=dict_p[source]

k=df.iloc[a,1:3]
coords_1=(k["long"],k["lati"])

import sys
class Graph(): 
    global coords_1
    def __init__(self, vertices):       
        self.V = vertices 
        print(self.V)
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)] 
    def printSolution(self, dist): 
        print("Vertex \tDistance from Source")
        for node in range(self.V): 
            print(node, "\t", dist[node] )   
    def minDistance(self, dist, sptSet): 
        min = 999999
        for v in range(self.V): 
            if dist[v] < min and sptSet[v] == False: 
                min = dist[v] 
                min_index = v 
        return min_index 
    def dijkstra(self, src): 
        global coords_1
        dist = [999999] * self.V 
        dist[src] = 0
        sptSet = [False] * self.V   
        for _ in range(self.V): 
            u = self.minDistance(dist, sptSet) 
            sptSet[u] = True
            k=df.iloc[u,1:3]
            coords_2=(k["long"],k["lati"])
            folium.PolyLine(locations = [coords_1, coords_2],line_opacity = 0.5).add_to(folium_map)  
            coords_1=coords_2
            for v in range(self.V): 
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]: 
                        dist[v] = dist[u] + self.graph[u][v] 
  
        self.printSolution(dist) 
  
# Driver program 
g = Graph(len(data)) 
g.graph = distance 

g.dijkstra(a)
folium_map.save("index.html")

import webbrowser
import os
file=os.path.abspath("index.html")
url = "file://"+file
webbrowser.register('chrome',None,webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
webbrowser.get('chrome').open(url)

