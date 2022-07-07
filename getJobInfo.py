import json
import random as rd
import requests as rq
import xml.etree.ElementTree as ET

API_KEY = 'WNL4OZ8N08QY72CDY0RT22VR1HJ'
RETURN_TYPE = 'XML'

# declare dicts
headerDict = {}
paramDict = {}

# { jobCd : [jobNm, jobClcd, jobClcdNM] }
norSrchDict = {}  # 일반직업
spclSrchDict = {}  # 이색직업
thmSrchDict = {}  # 테마별
newSrchDict = {}  # 신직업 dict


def set_default_dict():
    headerDict.clear()
    paramDict.clear()
    set_param_dict('authKey', API_KEY)
    set_param_dict('returnType', RETURN_TYPE)


def set_param_dict(key, value):
    paramDict.setdefault(key, value)


def get_job_theme(URI):
    headerDict.clear()
    paramDict.clear()

    # setting params
    set_param_dict('target', 'JOBDTL')
    set_param_dict('jobGb', '4')


# 일반직업상세 GET
def get_job_detail():
    set_default_dict()

    # set local variable
    keyList = list(norSrchDict.keys())

    # setting URI & params
    URI = 'http://openapi.work.go.kr/opi/opi/opia/jobSrch.do'
    set_param_dict('target', 'JOBDTL')
    set_param_dict('jobGb', '1')
    set_param_dict('dtlGb', '1')

    # Looping get call ( 350 calls )
    for key in keyList:
        majorCdList, majorNmList, certNmList = [], [], []
        majorCd, majorNm, certNm = '', '', ''

        paramDict['jobCd'] = key

        requestData = rq.get(URI, headers=headerDict, params=paramDict)

        # parsing XML
        root = ET.fromstring(requestData.text)

        jobCd = root.find('jobCd').text if root.find('jobCd') != -1 else None
        jobLrclNm = root.find('jobLrclNm').text if root.find('jobLrclNm') != -1 else None
        jobMdclNm = root.find('jobMdclNm').text if root.find('jobMdclNm') != -1 else None
        jobSmclNm = root.find('jobSmclNm').text if root.find('jobSmclNm') != -1 else None
        jobSum = root.find('jobSum').text if root.find('jobSum') != -1 else None
        way = root.find('way').text if root.find('way') != -1 else None

        relMajorList = root.findall('relMajorList') if root.find('relMajorList') != -1 else None
        if relMajorList != None and relMajorList != []:
            for relMajor in relMajorList:
                majorCd = relMajor.find('majorCd').text
                majorNm = relMajor.find('majorNm').text
                majorCdList.append(majorCd)
                majorNmList.append(majorNm)

            majorCd = ', '.join(majorCdList)
            majorNm = ', '.join(majorNmList)

        relCertList = root.findall('relCertList') if root.find('relCertList') != -1 else None
        if relCertList != None and relCertList != []:
            for relCert in relCertList:
                certNm = relCert.find('certNm').text
                certNmList.append(certNm)

            certNm = ', '.join(certNmList)

        sal = root.find('sal').text if root.find('sal') != -1 else None
        jobSatis = root.find('jobSatis').text if root.find('jobSatis') != -1 else None
        jobProspect = root.find('jobProspect').text if root.find('jobProspect') != -1 else None
        jobStatus = root.find('jobStatus').text if root.find('jobStatus') != -1 else None
        jobAbil = root.find('jobAbil').text if root.find('jobAbil') != -1 else None
        jobVals = root.find('jobVals').text if root.find('jobVals') != -1 else None
        jobActvImprtncs = root.find('jobActvImprtncs').text if root.find('jobActvImprtncs') != -1 else None
        jobActvLvls = root.find('jobActvLvls').text if root.find('jobActvLvls') != -1 else None

        # Nonetype exception
        # knowldg = root.find('knowldg').text if root.find('knowldg') != -1 else None
        # jobEnv = root.find('jobEnv').text if root.find('jobEnv') != -1 else None
        # jobChr = root.find('jobChr').text if root.find('jobChr') != -1 else None
        # jobIntrst = root.find('jobIntrst').text if root.find('jobIntrst') != -1 else None # MBTI 랑 엮을 수 있나?



        # print(jobCd, jobLrclNm, jobMdclNm, jobSmclNm, jobSum, way, majorCd, majorNm, certNm, end='\n========================================================================\n')




# 직업목록 GET
def get_job_srch():
    set_default_dict()

    # setting URI & params
    URI = 'http://openapi.work.go.kr/opi/opi/opia/jobSrch.do'
    set_param_dict('target', 'JOBCD')
    # API get call
    requestData = rq.get(URI, headers=headerDict, params=paramDict)

    # xml parsing
    jobSrch = ET.fromstring(requestData.text)
    # looping parsed xml to extract text
    for jobList in jobSrch.findall('jobList'):
        # normal job raise AttributeError
        try:
            jobGb = jobList.find('jobGb').text
        except (AttributeError):
            jobGb = ''

        jobClcd = jobList.find('jobClcd').text
        jobClcdNM = jobList.find('jobClcdNM').text
        jobCd = jobList.find('jobCd').text
        jobNm = jobList.find('jobNm').text

        # use 'in' to manage multiple jobGb
        if '3' in jobGb:
            spclSrchDict.setdefault(jobCd, [jobGb, jobNm, jobClcd, jobClcdNM])
        if '4' in jobGb:
            thmSrchDict.setdefault(jobCd, [jobGb, jobNm, jobClcd, jobClcdNM])
        if '6' in jobGb:
            newSrchDict.setdefault(jobCd, [jobGb, jobNm, jobClcd, jobClcdNM])
        if jobGb == '':
            norSrchDict.setdefault(jobCd, [jobGb, jobNm, jobClcd, jobClcdNM])


# 학과정보 GET
def get_major_srch():
    return True


# 직업전망 GET
def get_job_prospect():
    return True


# 직업사전 GET
def get_job_dic():
    return True


# 공채속보 GET
def get_open_emp_info():
    return True


# 표준직무기술서 GET
def get_job_by_word():
    return True


# 직무데이터사전 API
def get_dic_data_by_word():
    return True


# 항상 호출하여 Source 받아 dict에 저장해 놓는 것이 좋음
get_job_srch()
get_job_detail()
