from typing import Literal
import pandas as pd
import re

#df = pd.read_excel("timetableDate.xlsx")

#cos_time, brief
#F34-EC122[GF],Mabc-EC220[GF],Mabc-EC221[GF],Mabc-EC222[GF]
#M12345678W12345678R1234-
#跨院基本素養(106),核心通識-藝術與文化(90),領域課程-人文與美學(110)
#cos_time = df['cos_time'].to_list()
#brief = df['brief'].to_list()


WEEK = ['M', 'T', 'W', 'R', 'F', 'S', 'U']
#['time','class','campus']
Template = ['time','class','campus']
def time_setter(string):
    #print(string)
    ret_str = ""
    temp = ""
    for j in string:
        if j in WEEK:
            temp = j
        else:
            ret_str += temp + j
    return ret_str

def time_slicer(data: str):
    pattern = r"([A-Za-z0-9]+)|-([A-Z0-9]+)|\[([A-Z]+)\]"
    l = data.split(",")
    base = {'time': [], 'class': [], "campus": []}
    for string in l:
        #print(string)
        matches = re.findall(pattern, string)
        for m in matches:
            if m[0]: base["time"].append(time_setter(m[0]))
            if m[1]: base['class'].append(m[1])
            if m[2]: base['campus'].append(m[2])
    
    return base

#N^2 見表，O1查詢
#F34-EC122[GF],Mabc-EC220[GF],Mabc-EC221[GF],Mabc-EC222[GF]
#M12345678W12345678R1234-
#time_slicer("F34-EC122[GF],Mabc-EC220[GF],Mabc-EC221[GF],Mabc-EC222[GF]")

def pre():
    df = pd.read_excel("timetableDate.xlsx")
    df["cos_data"] = df["cos_time"].apply(time_slicer)
    return df


CONDITION = ['time','campus','class','type']
condition_lit = Literal['time','campus','class','type']
campus_lit = Literal['YM','BA','GF','BM','GR','LJ']
#class_lit = Literal['']
TYPE_CONST = ['性平相關課程', '核心通識-哲學與心靈', '基本素養-組織管理', '基本素養-量性推理', '開放隨班附讀', '媒體資訊判讀', '博雅選修通識', '大型展演', '通識校基本素養', '書報專題討論', 'nan', '遠距課程', '通識核心課程', '社會參與', '領域課程-公民與倫理思考', '人權教育', '大學專題', '音樂指導(個別指導費)', '程式相關', '一般實習', '專題演講', '跨校區課程', '實驗課程', '基礎服務學習', '領域課程-社會中的科技與自然', '寫作課程', '語言與溝通-英文', '生命教育', '語言與溝通-第二外語', '核心通識-社會與經濟', '人文關懷', '語言與溝通-溝通表達', 'OCW', '通識跨院基本素養', '領域課程-人文與美學', '專業服務學習', '領域課程-個人、社會與文化', '不支援核心', '大學導師', '智財權課程', '語言領域-中文(含寫作)', '基本素養-生命及品格教育', '核心通識-藝術與文化', '核心通識-科技與社會', '核心通識-倫理與道德思考', '品德教育', '語言領域-英文', '核心通識-歷史與文明', '基本素養-批判思考']
type_lit = Literal['性平相關課程', '核心通識-哲學與心靈', '基本素養-組織管理', '基本素養-量性推理', '開放隨班附讀', '媒體資訊判讀', '博雅選修通識', '大型展演', '通識校基本素養', '書報專題討論', 'nan', '遠距課程', '通識核心課程', '社會參與', '領域課程-公民與倫理思考', '人權教育', '大學專題', '音樂指導(個別指導費)', '程式相關', '一般實習', '專題演講', '跨校區課程', '實驗課程', '基礎服務學習', '領域課程-社會中的科技與自然', '寫作課程', '語言與溝通-英文', '生命教育', '語言與溝通-第二外語', '核心通識-社會與經濟', '人文關懷', '語言與溝通-溝通表達', 'OCW', '通識跨院基本素養', '領域課程-人文與美學', '專業服務學習', '領域課程-個人、社會與文化', '不支援核心', '大學導師', '智財權課程', '語言領域-中文(含寫作)', '基本素養-生命及品格教育', '核心通識-藝術與文化', '核心通識-科技與社會', '核心通識-倫理與道德思考', '品德教育', '語言領域-英文', '核心通識-歷史與文明', '基本素養-批判思考']


def find(df: pd.DataFrame, condition: str = "M3"):
    df_temp = df[df['cos_data'].apply(lambda x: any(condition in time for time in x['time']))]
    df_temp.to_excel("HI2.xlsx")


def find_ori(df: pd.DataFrame, condition: condition_lit, condi_args: str):
    if isinstance(condi_args, list): condi_args = '|'.join(condi_args)
    match condition:
        case 'campus'| 'class' | 'time' as condi:
            df_temp = df[df['cos_data'].apply(lambda x: any(c_arg in time for time in x.split() for c_arg in condi_args) if isinstance(x, str) else any(c_arg in time for time in x[condi] for c_arg in condi_args))]

        case "type":
            df_temp = df[df['brief'].str.contains(condi_args, na=False)]
    return df_temp

def find_condi():
    df = pd.read_excel("timetableDate.xlsx")
    ss = set()
    for i in df['brief']:
        l = str(i).split(",")
        for j in l:
            ss.add(j.split('_')[0])
    return ss

def main():
    df = pd.read_excel("timetableDate.xlsx")
    df = find_ori(df,'time','M3')
    df = find_ori(df,'campus',["GF","YM"])
    df = find_ori(df, 'type', ["實驗課程","程式相關"])
    df.to_excel("HI.xlsx")

if __name__ == "__main__":
    main()
    pass