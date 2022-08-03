# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색
import csv
import os
import sys
import urllib.request

serviceList = ['blog', 'news', 'book', 'encyc', 'cafearticle', 'kin', 'webkr', 'doc']
keywordList = ['사업관리 직무', '경영 직무', '회계 직무', '사무 직무', '금융 직무', '보험 직무', '교육 직무', '자연 직무', '사회과학 직무',
               '법률 직무', '경찰 직무', '소방 직무', '교도 직무', '국방 직무', '보건 직무', '의료 직무', '사회복지 직무', '종교 직무',
               '문화 직무', '예술 직무', '디자인 직무', '방송 직무', '운전 직무', '운송 직무', '영업판매 직무', '경비 직무', '청소 직무',
               '이용 직무', '숙박 직무', '여행 직무', '오락 직무', '스포츠 직무', '음식서비스 직무', '건설 직무', '기계 직무', '재료 직무',
               '화학 직무', '바이오 직무', '섬유 직무', '의복 직무', '전기 직무', '전자 직무', '정보통신 직무', '식품가공 직무', '인쇄 직무',
               '목재 직무', '가구 직무', '공예 직무', '환경 직무', '에너지 직무', '안전 직무', '농림어업 직무']
client_id = "Q7GCxEYLAF1KhR9Szgtg"
client_secret = "X01Hozom9d"
displayNum = 100


def write_csv(_fname, _result):
    f = open('./json_results/{0}'.format(_fname), 'w', newline='')
    f.write(_result)
    f.close()


for keyword in keywordList:
    encText = urllib.parse.quote(keyword)
    for service in serviceList:
        url = "https://openapi.naver.com/v1/search/" + service + ".json?query=" + encText + "&display=" + str(
            displayNum)  # json 결과

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if (rescode == 200):
            response_body = response.read()
            result = response_body.decode('utf-8')
            fname = keyword + '_' + service + '.txt'
            write_csv(fname, result)
            # print(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)
