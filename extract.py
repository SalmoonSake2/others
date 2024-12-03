from typing import Literal
import pandas as pd
import re
import ast

WEEK = ['M', 'T', 'W', 'R', 'F', 'S', 'U']
CONDITION = ['time','campus','class','type']
condition_lit = Literal['time','campus','class','type']
campus_lit = Literal['YM','BA','GF','BM','GR','LJ']
#class_lit = Literal['']
TYPE_CONST = ['性平相關課程', '核心通識-哲學與心靈', '基本素養-組織管理', '基本素養-量性推理', '開放隨班附讀', '媒體資訊判讀', '博雅選修通識', '大型展演', '通識校基本素養', '書報專題討論', 'nan', '遠距課程', '通識核心課程', '社會參與', '領域課程-公民與倫理思考', '人權教育', '大學專題', '音樂指導(個別指導費)', '程式相關', '一般實習', '專題演講', '跨校區課程', '實驗課程', '基礎服務學習', '領域課程-社會中的科技與自然', '寫作課程', '語言與溝通-英文', '生命教育', '語言與溝通-第二外語', '核心通識-社會與經濟', '人文關懷', '語言與溝通-溝通表達', 'OCW', '通識跨院基本素養', '領域課程-人文與美學', '專業服務學習', '領域課程-個人、社會與文化', '不支援核心', '大學導師', '智財權課程', '語言領域-中文(含寫作)', '基本素養-生命及品格教育', '核心通識-藝術與文化', '核心通識-科技與社會', '核心通識-倫理與道德思考', '品德教育', '語言領域-英文', '核心通識-歷史與文明', '基本素養-批判思考']
type_lit = Literal['性平相關課程', '核心通識-哲學與心靈', '基本素養-組織管理', '基本素養-量性推理', '開放隨班附讀', '媒體資訊判讀', '博雅選修通識', '大型展演', '通識校基本素養', '書報專題討論', 'nan', '遠距課程', '通識核心課程', '社會參與', '領域課程-公民與倫理思考', '人權教育', '大學專題', '音樂指導(個別指導費)', '程式相關', '一般實習', '專題演講', '跨校區課程', '實驗課程', '基礎服務學習', '領域課程-社會中的科技與自然', '寫作課程', '語言與溝通-英文', '生命教育', '語言與溝通-第二外語', '核心通識-社會與經濟', '人文關懷', '語言與溝通-溝通表達', 'OCW', '通識跨院基本素養', '領域課程-人文與美學', '專業服務學習', '領域課程-個人、社會與文化', '不支援核心', '大學導師', '智財權課程', '語言領域-中文(含寫作)', '基本素養-生命及品格教育', '核心通識-藝術與文化', '核心通識-科技與社會', '核心通識-倫理與道德思考', '品德教育', '語言領域-英文', '核心通識-歷史與文明', '基本素養-批判思考']

def find(df: pd.DataFrame, condition: condition_lit, condi_args: str| list[str]):
    if isinstance(condi_args, str): condi_args = [condi_args]
    match condition:
        case 'campus'| 'class' | 'time' as condi:
            df_temp = df[df['cos_data'].apply(lambda x: any(c_arg in i for i in ast.literal_eval(x)[condi] for c_arg in condi_args))]

        case "type":
            df_temp = df[df['brief'].apply(lambda x: any(c_arg in i for i in ast.literal_eval(x) for c_arg in condi_args))]
    return df_temp

def main():
    df = pd.read_excel("timetableDate.xlsx")
    df = find(df,'time',["M3","M4","T3","T4"])
    df = find(df,'campus',["GF"])
    df = find(df, 'type', ["實驗課程","領域課程-人文與美學"])
    df.to_excel("extract.xlsx")

if __name__ == "__main__":
    main()
    pass