'''
nycu_courses_fetcher.py

author:

Azusa Kaze
Salmoon Sake
'''


import requests
import pandas as pd

def analyze_json(js:dict,df:dict) -> None:
    '''
    將輸入的json(實為字典)進行解析，提取需要的資訊後存入字典
    '''

    if not js:return

    #逐一讀取不同學院/系所的課表
    for institude in js.values():

        #"1"大致儲存該學院所有課程的主要資訊
        #備註：這命名超爛，網頁誰寫的?
        courses_dict = institude["1"]

        #將課程的"本期課號"當作key去逐一處理學院的所有課程
        for course_key in courses_dict:
            course = courses_dict[course_key]
            course_id = course_key

            #如果已經紀錄了，就直接跳過
            if course_id in df: 
                continue

            #將主要資訊填入暫存的字典
            course_name = course["cos_cname"]
            course_credit = course["cos_credit"]
            course_hour = course["cos_hours"]
            course_teacher = course["teacher"]
            course_time = course["cos_time"]
            memo = course["memo"]

            series = [course_name,course_credit,course_hour,course_teacher,course_time,None,memo]
            df[course_id] = series
        
        #再從"costype"取得課程屬性
        #不懂幹嘛分開儲存，一起放在"1"之下不香嗎?
        course_type_dict = institude["costype"]

        #逐一讀取課程屬性(必修、核心通識、領域課程...)
        for course_key in course_type_dict:
            course_types = [course_type for course_type in course_type_dict[course_key]]

            #第[5]項代表課程類型(這也是之前設為None留空的原因)
            df[course_key][5] = course_types
        
    return df

def download_nycu_course(file:str) -> None:
    '''
    將陽明交通當期課表下載成excel
    '''

    #課表查詢系統的url
    URL = "https://timetable.nycu.edu.tw/"

    #發出請求的url
    PARAMS = {"r": "main/get_cos_list"}

    #header設定
    HEADER = {'user-agent': 'Mozilla/5.0'}

    #輸入資料
    payload = {"m_acy":113,
            "m_sem":1,
            "m_acyend":113,
            "m_semend":1,
            "m_dep_uid":"**",
            "m_group":"**",
            "m_grade":"**",
            "m_class":"**",
            "m_option":"crstime",
            "m_crsname":"**",
            "m_teaname":"**",
            "m_cos_id":"**",
            "m_cos_code":"**",
            "m_crstime":"**",
            "m_crsoutline":"**",
            "m_costype":"**",
            "m_selcampus":"**"}
    
    #陽明課表的時間代號，由於網頁限制，不能送出過多時間
    DAY_INDEX = ("My,Mz,M1,M2,M3,M4",
                 "Mn,M5,M6,M7,M8",
                 "M9,Ma,Mb,Mc,Md",
                 "Ty,Tz,T1,T2,T3,T4",
                 "Tn,T5,T6,T7,T8",
                 "T9,Ta,Tb,Tc,Td",
                 "Wy,Wz,W1,W2,W3,W4",
                 "Wn,W5,W6,W7,W8",
                 "W9,Wa,Wb,Wc,Wd",
                 "Ry,Rz,R1,R2,R3,R4",
                 "Rn,R5,R6,R7,R8",
                 "R9,Ra,Rb,Rc,Rd",
                 "Fy,Fz,F1,F2,F3,F4",
                 "Fn,F5,F6,F7,F8",
                 "F9,Fa,Fb,Fc,Fd",
                 "Sy,Sz,S1,S2,S3,S4",
                 "Sn,S5,S6,S7,S8",
                 "S9,Sa,Sb,Sc,Sd",
                 "Uy,Uz,U1,U2,U3,U4",
                 "Un,U5,U6,U7,U8",
                 "U9,Ua,Ub,Uc,Ud")

    #創建用於儲存課程資訊的字典(key:本期課號，vlaue:屬性)
    df = dict()

    #從所有時段逐一查詢
    for time_slot in DAY_INDEX:

        #設定輸入時間
        payload["m_crstime"] = time_slot

        #擷取課表資料的JSON
        js:dict = requests.post(url=URL,data=payload,params=PARAMS,headers=HEADER).json()

        #分析JSON並儲存到字典中
        analyze_json(js,df)

    #將字典中的課程全數輸出到excel中
    pddf = pd.DataFrame(df).T
    pddf.to_excel(file,index=False)