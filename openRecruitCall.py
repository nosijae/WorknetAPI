import requests as rq

callURL = 'http://openapi.work.go.kr/opi/opi/opia/korJobDicApi.do'

# declare header & params dict
headerDict = {}
paramDict = {}

# Setting Param
paramDict.setdefault('authKey', 'WNL4OZ8N08QY72CDY0RT22VR1HJ')
paramDict.setdefault('returnType', 'XML')
paramDict.setdefault('startType', 1)
paramDict.setdefault('display', 10)
paramDict.setdefault('target', 'dJobCD')
paramDict.setdefault('srchType', 'EL')
paramDict.setdefault('eduLevel', '6')


# paramDict.setdefault('callTp', 'L')

# call API
requestData = rq.get(callURL, headers=headerDict, params=paramDict)


# Write Result on HTML File
internRst = open('./results/jobVision.html', 'w', encoding='UTF-8')
internRst.writelines(requestData.text)
internRst.close()
