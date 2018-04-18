import json
import urllib

class GetData:
    region_top = "http://www.kma.go.kr/DFSROOT/POINT/DATA/top.json.txt"

    top = ""
    mdl = ""
    leaf = ""

    top_code = ""
    mdl_code = ""
    service_key = ""

    x = ""
    y = ""

    date = ""
    time = ""
    def __init__(self, top, mdl, leaf, service_key):
        self.top = top
        self.mdl = mdl
        self.leaf = leaf
        self.service_key = service_key

    def setRegion(self):
        u = urllib.request.urlopen(self.region_top).read()
        json_top = json.loads(u)
        for i in json_top:
            if str(self.top) == str(i["value"]):
                self.top_code = i["code"]
                break
            else:
                self.top_code = "11"
        u = urllib.request.urlopen("http://www.kma.go.kr/DFSROOT/POINT/DATA/mdl." + str(self.top_code) + ".json.txt").read()
        json_mdl = json.loads(u)
        for i in json_mdl:
            if str(self.mdl) == str(i["value"]):
                self.mdl_code = i["code"]
                break
            else:
                self.mdl_code = "11650"
        u = urllib.request.urlopen("http://www.kma.go.kr/DFSROOT/POINT/DATA/leaf." + str(self.mdl_code) + ".json.txt").read()
        json_leaf = json.loads(u)
        for i in json_leaf:
            if str(self.leaf) == str(i["value"]):
                self.x = str(i["x"])
                self.y = str(i["y"])
                break
            else:
                self.x = "61"
                self.y = "125"

    def setTime(self, date, time):
        self.date = date
        self.time = time

    def getData(self):
        url1 = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastTimeData?&ServiceKey=" + str(self.service_key) + "&base_date=" + str(self.date) + "&base_time=" + str(self.time)
        url2 = "&nx=" + self.x + "&ny=" + self.y + "&numOfRows=20&pageNo=1&_type=json"
        print(url1 + url2)
        u = urllib.request.urlopen(url1 + url2).read()
        json_data = json.loads(u)
        return json_data