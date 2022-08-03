import requests as rq
import xml.etree.ElementTree as ET


API_KEY = 'WNL4OZ8N08QY72CDY0RT22VR1HJ'
RETURN_TYPE = 'XML'

# declare dicts
headerDict = {}
paramDict = {}

keywords = ['사업관리', '경영', '회계', '금융', '교육·자연·사회과학',
            '법률·경찰·소방·교도·국방', '보건·의료', '사회복지·종교', '문화·예술·디자인·방송',
            '운전·운송', '영업판매', '경비·청소', '이용·숙박·여행·오락·스포츠', '음식서비스',
            '건설', '기계', '재료', '화학·바이오', '섬유·의복', '전기·전자', '정보통신',
            '식품가공', '인쇄·목재·가구·공예', '환경·에너지·안전', '농림어업']


# default set Dictionary
def set_default_dict():
    headerDict.clear()
    paramDict.clear()
    set_param_dict('authKey', API_KEY)
    set_param_dict('returnType', RETURN_TYPE)


# set Dictonary parameter
def set_param_dict(key, value):
    paramDict.setdefault(key, value)


def get_dic_data():
    # setting URI & params
    URI = 'http://openapi.work.go.kr/opi/opi/opia/dicDataByWordApi.do'

    for keyword in keywords:
        set_default_dict()
        set_param_dict('word', keyword)
        # API get call
        requestData = rq.get(URI, headers=headerDict, params=paramDict)

        # xml parsing (fromstring()은 문자열에서 Element로 XML을 직접 구문 분석)
        requestData = requestData.json()
        try:
            print(requestData['result'])
        except:
            print('err')


def get_dic_data_by_code():
    URI = 'http://openapi.work.go.kr/opi/opi/opia/dicDataByCodeApi.do'




get_dic_data()
