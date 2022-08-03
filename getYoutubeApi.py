from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

keywordList = ['사업관리 직무', '경영 직무', '회계 직무', '사무 직무', '금융 직무', '보험 직무', '교육 직무', '자연 직무', '사회과학 직무',
               '법률 직무', '경찰 직무', '소방 직무', '교도 직무', '국방 직무', '보건 직무', '의료 직무', '사회복지 직무', '종교 직무',
               '문화 직무', '예술 직무', '디자인 직무', '방송 직무', '운전 직무', '운송 직무', '영업판매 직무', '경비 직무', '청소 직무',
               '이용 직무', '숙박 직무', '여행 직무', '오락 직무', '스포츠 직무', '음식서비스 직무', '건설 직무', '기계 직무', '재료 직무',
               '화학 직무', '바이오 직무', '섬유 직무', '의복 직무', '전기 직무', '전자 직무', '정보통신 직무', '식품가공 직무', '인쇄 직무',
               '목재 직무', '가구 직무', '공예 직무', '환경 직무', '에너지 직무', '안전 직무', '농림어업 직무']

DEVELOPER_KEY = "AIzaSyBWOdlOMsfSRMkNt44act6wWzpyxo7Sa3A"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def write_file(_fname, _result):
    f = open('./youtube_json_results/{0}'.format(_fname), 'w', newline='')
    f.write(_result)
    f.close()


youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

search_response = youtube.search().list(
    q='법률 직무',
    part="id,snippet",
    maxResults=30
).execute()

print(search_response)
write_file('법률 직무.json', search_response)

# for keyword in keywordList:
#     search_response = youtube.search().list(
#         q=keyword,
#         part="id,snippet",
#         maxResults=30
#     ).execute()
#
#     print(search_response)
#     write_file(keyword + '.json', search_response)
