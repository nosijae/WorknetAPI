import csv
import pandas as pd
import numpy as np
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

# save API results
jobInfoList = []


def csv_to_xlsx():
    r_csv = pd.read_csv('./results/job_info.csv')

    save_xlsx = pd.ExcelWriter('./results/job_info.xlsx')
    r_csv.to_excel(save_xlsx, index=False)

    save_xlsx.save()
    save_xlsx.close()


def write_job_csv():
    f = open('./results/job_info.csv', 'w', newline='')
    wr = csv.writer(f)

    _header = ["직업코드", "직업 대분류명", "직업 중분류명", "직업 소분류명", "하는일", "되는길",
               "관련 전공 코드", "관련 전공명", "관련자격증명", "임금", "직업만족도", "일자리전망",
               "일자리현황", "업무수행능력", "지식", "업무환경", "성격", "흥미", "직업 가치관",
               "업무활동 중요도", "업무활동 수준"]

    wr.writerow(_header)

    for jobInfo in jobInfoList:
        wr.writerow(jobInfo)

    f.close()

    csv_to_xlsx()


# default set Dictionary
def set_default_dict():
    headerDict.clear()
    paramDict.clear()
    set_param_dict('authKey', API_KEY)
    set_param_dict('returnType', RETURN_TYPE)


# set Dictonary parameter
def set_param_dict(key, value):
    paramDict.setdefault(key, value)


# def get_job_theme():
#     headerDict.clear()
#     paramDict.clear()
#
#     # setting params
#     set_param_dict('target', 'JOBDTL')
#     set_param_dict('jobGb', '4')


# get from xml ( non-error data )
def find_normal_target(root, target):
    rstStr = root.find(target).text if root.find(target) != - 1 else None
    return rstStr


# get from xml ( none type exception )
def handle_none_exception(root, target):
    rstStr = root.find(target) if root.find(target) != -1 else None

    if rstStr == None:
        rstStr = None
    else:
        rstStr = rstStr.text

    return rstStr


# 일반직업상세 GET
def get_job_detail():
    set_default_dict()

    # get Cd from normal detail category
    cdList = list(norSrchDict.keys())

    # setting URI & params
    URI = 'http://openapi.work.go.kr/opi/opi/opia/jobSrch.do'
    set_param_dict('target', 'JOBDTL')
    set_param_dict('jobGb', '1')
    set_param_dict('dtlGb', '1')

    # Looping get call ( 350 calls )
    for cd in cdList:
        majorCd, majorNm, certNm = '', '', ''

        paramDict['jobCd'] = cd

        requestData = rq.get(URI, headers=headerDict, params=paramDict)

        # parsing XML
        root = ET.fromstring(requestData.text)

        # normal Operation
        jobCd = find_normal_target(root, 'jobCd')
        jobLrclNm = find_normal_target(root, 'jobLrclNm')
        jobMdclNm = find_normal_target(root, 'jobMdclNm')
        jobSmclNm = find_normal_target(root, 'jobSmclNm')
        jobSum = find_normal_target(root, 'jobSum')
        way = find_normal_target(root, 'way')
        sal = find_normal_target(root, 'sal')
        jobSatis = find_normal_target(root, 'jobSatis')
        jobProspect = find_normal_target(root, 'jobProspect')
        jobStatus = find_normal_target(root, 'jobStatus')
        jobAbil = find_normal_target(root, 'jobAbil')
        jobVals = find_normal_target(root, 'jobVals')
        jobActvImprtncs = find_normal_target(root, 'jobActvImprtncs')
        jobActvLvls = find_normal_target(root, 'jobActvLvls')

        # using iter method to find sub tree
        for relMajor in root.iter('relMajorList'):
            majorCd += relMajor.find('majorCd').text + '/'
            majorNm += relMajor.find('majorNm').text + '/'

        for relCert in root.iter('relCertList'):
            certNm += relCert.find('certNm').text + '/'

        # handle Attribute(Nonetype) exception
        knowldg = handle_none_exception(root, 'knowldg')
        jobEnv = handle_none_exception(root, 'jobEnv')
        jobChr = handle_none_exception(root, 'jobChr')
        jobIntrst = handle_none_exception(root, 'jobIntrst')

        results = [jobCd, jobLrclNm, jobMdclNm, jobSmclNm, jobSum, way,
                   majorCd, majorNm, certNm, sal, jobSatis, jobProspect,
                   jobStatus, jobAbil, knowldg, jobEnv, jobChr, jobIntrst, jobVals,
                   jobActvImprtncs, jobActvLvls]

        jobInfoList.append(results)

    write_job_csv()


# 직업목록 GET
def get_job_srch():
    set_default_dict()

    # setting URI & params
    URI = 'http://openapi.work.go.kr/opi/opi/opia/jobSrch.do'
    set_param_dict('target', 'JOBCD')
    # API get call
    requestData = rq.get(URI, headers=headerDict, params=paramDict)

    # xml parsing (fromstring()은 문자열에서 Element로 XML을 직접 구문 분석)
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


# # 학과정보 GET
# def get_major_srch():
#     return True
#
#
# # 직업전망 GET
# def get_job_prospect():
#     return True
#
#
# # 직업사전 GET
# def get_job_dic():
#     return True
#
#
# # 공채속보 GET
# def get_open_emp_info():
#     return True
#
#
# # 표준직무기술서 GET
# def get_job_by_word():
#     return True
#
#
# # 직무데이터사전 API
# def get_dic_data_by_word():
#     return True


# 항상 호출하여 Source 받아 dict에 저장해 놓는 것이 좋음
get_job_srch()
get_job_detail()
