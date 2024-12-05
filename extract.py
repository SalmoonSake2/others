from typing import Literal
import pandas as pd
import re
import ast

WEEK = ['M', 'T', 'W', 'R', 'F', 'S', 'U']
TIME = ['y', 'z', '1', '2', '3', '4', 'n', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd']
CONDITION = ['time','campus','class','type']
condition_lit = Literal['time','campus','class','type']
CAMPUS_CONST = ['YM','BA','GF','BM','GR','LJ']
campus_lit = Literal['YM','BA','GF','BM','GR','LJ']
TYPE_CONST = ['', '跨校區課程', '基礎服務學習', '通識核心課程', '核心通識-科技與社會', '通識校基本素養', '大學導師', '通識跨院基本素養', 'OCW', '品德教育', '語言與溝通-第二外語', '開放隨班附讀', '基本素養-組織管理', '音樂指導(個別指導費)', '專題演講', '遠距課程', '人權教育', '生命教育', '程式相關', '語言與溝通-英文', '媒體資訊判讀', '領域課程-人文與美學', '基本素養-量性推理', '核心通識-藝術與文化', '大型展演', '一般實習', '實驗課程', '核心通識-哲學與心靈', '核心通識-歷史與文明', '智財權課程', '寫作課程', '書報專題討論', '核心通識-倫理與道德思考', '專業服務學習', '領域課程-個人、社會與文化', '大學專題', '基本素養-生命及品格教育', '博雅選修通識', '不支援核心', '領域課程-社會中的科技與自然', '語言與溝通-溝通表達', '語言領域-中文(含寫作)', '性平相關課程', '基本素養-批判思考', '核心通識-社會與經濟', '語言領域-英文', '人文關懷', '社會參與', '領域課程-公民與倫理思考']
type_lit = Literal['', '跨校區課程', '基礎服務學習', '通識核心課程', '核心通識-科技與社會', '通識校基本素養', '大學導師', '通識跨院基本素養', 'OCW', '品德教育', '語言與溝通-第二外語', '開放隨班附讀', '基本素養-組織管理', '音樂指導(個別指導費)', '專題演講', '遠距課程', '人權教育', '生命教育', '程式相關', '語言與溝通-英文', '媒體資訊判讀', '領域課程-人文與美學', '基本素養-量性推理', '核心通識-藝術與文化', '大型展演', '一般實習', '實驗課程', '核心通識-哲學與心靈', '核心通識-歷史與文明', '智財權課程', '寫作課程', '書報專題討論', '核心通識-倫理與道德思考', '專業服務學習', '領域課程-個人、社會與文化', '大學專題', '基本素養-生命及品格教育', '博雅選修通識', '不支援核心', '領域課程-社會中的科技與自然', '語言與溝通-溝通表達', '語言領域-中文(含寫作)', '性平相關課程', '基本素養-批判思考', '核心通識-社會與經濟', '語言領域-英文', '人文關懷', '社會參與', '領域課程-公民與倫理思考']

def find(df: pd.DataFrame, condition: condition_lit, condi_args: str| list[str]):
    """擷取資料

    Parameters
    ----------
    df : pd.DataFrame
        資料總表
    condition : condition_lit
        資料種類
    condi_args : str | list[str]
        資料細項

    Returns
    -------
    pd.DataFrame
        已擷取資料回傳
    """
    if isinstance(condi_args, str): condi_args = [condi_args]
    match condition:
        case 'campus'| 'class' | 'time':
            df_temp = df[df['cos_data'].apply(lambda x: any(c_arg in str(x) for c_arg in condi_args))]

        case "type":
            df_temp = df[df['brief'].apply(lambda x: any(c_arg in str(x) for c_arg in condi_args))]
    return df_temp

def main():
    """範例

    Returns
    -------
    pd.DataFrame
        回傳資料
    """
    df = pd.read_excel("timetableDate.xlsx", index_col=0)
    df = find(df,'time',["M3","M4","T3","T4","T5","T6",'Tc', 'Td', 'Wy', 'Wz', 'W1', 'W2', 'W3', 'W4', 'Wn', 'W5', 'W6', 'W7', 'W8', 'W9', 'Wa', 'Wb', 'Wc', 'Wd', 'Ry', 'Rz', 'R1', 'R2', 'R3'])
    df = find(df,'campus',["GF","YM"])
    df = find(df, 'type', ["實驗課程","領域課程-人文與美學"])
    df.to_excel("extract.xlsx")
    return df

if __name__ == "__main__":
    print(main())
    pass