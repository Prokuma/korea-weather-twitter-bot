import json
import urllib
import codecs

class GetData:
    reader = codecs.getreader("utf-8")
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

    # 지정 지역의 좌표 받아오기
    def setRegion(self):
        # 특별시/광역시/도
        u = urllib.request.urlopen(self.region_top).read().decode('utf-8')
        json_top = json.loads(u)
        for i in json_top:
            if str(self.top) == str(i["value"]):
                self.top_code = i["code"]
                break
            else:
                self.top_code = "11"

        # 시/군/구
        u = urllib.request.urlopen("http://www.kma.go.kr/DFSROOT/POINT/DATA/mdl." + str(self.top_code) + ".json.txt").read().decode('utf-8')
        json_mdl = json.loads(u)
        for i in json_mdl:
            if str(self.mdl) == str(i["value"]):
                self.mdl_code = i["code"]
                break
            else:
                self.mdl_code = "11650"

        # 동/읍/리
        u = urllib.request.urlopen("http://www.kma.go.kr/DFSROOT/POINT/DATA/leaf." + str(self.mdl_code) + ".json.txt").read().decode('utf-8')
        json_leaf = json.loads(u)
        for i in json_leaf:
            if str(self.leaf) == str(i["value"]):
                self.x = str(i["x"])
                self.y = str(i["y"])
                break
            else:
                self.x = "61"
                self.y = "125"

    # 현재시각 설정
    def setTime(self, date, time):
        self.date = date
        self.time = time

    # 데이터 요청
    def getData(self):
        url1 = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib?&ServiceKey=" + str(self.service_key) + "&base_date=" + str(self.date) + "&base_time=" + str(self.time)
        url2 = "&nx=" + self.x + "&ny=" + self.y + "&numOfRows=40&pageNo=1&_type=json"
        u = urllib.request.urlopen(url1 + url2).read().decode('utf-8')
        json_data = json.loads(u)
        return json_data