from typing import Literal
import pandas as pd
import re

condition_lit = Literal['time','campus','class','type']
TIME_CONST = ['My', 'Mz', 'M1', 'M2', 'M3', 'M4', 'Mn', 'M5', 'M6', 'M7', 'M8', 'M9', 'Ma', 'Mb', 'Mc', 'Md', 'Ty', 'Tz', 'T1', 'T2', 'T3', 'T4', 'Tn', 'T5', 'T6', 'T7', 'T8', 'T9', 'Ta', 'Tb', 'Tc', 'Td', 'Wy', 'Wz', 'W1', 'W2', 'W3', 'W4', 'Wn', 'W5', 'W6', 'W7', 'W8', 'W9', 'Wa', 'Wb', 'Wc', 'Wd', 'Ry', 'Rz', 'R1', 'R2', 'R3', 'R4', 'Rn', 'R5', 'R6', 'R7', 'R8', 'R9', 'Ra', 'Rb', 'Rc', 'Rd', 'Fy', 'Fz', 'F1', 'F2', 'F3', 'F4', 'Fn', 'F5', 'F6', 'F7', 'F8', 'F9', 'Fa', 'Fb', 'Fc', 'Fd', 'Sy', 'Sz', 'S1', 'S2', 'S3', 'S4', 'Sn', 'S5', 'S6', 'S7', 'S8', 'S9', 'Sa', 'Sb', 'Sc', 'Sd', 'Uy', 'Uz', 'U1', 'U2', 'U3', 'U4', 'Un', 'U5', 'U6', 'U7', 'U8', 'U9', 'Ua', 'Ub', 'Uc', 'Ud']
CAMPUS_CONST = ['YM','BA','GF','BM','GR','LJ']
TYPE_CONST = ['', '跨校區課程', '基礎服務學習', '通識核心課程', '核心通識-科技與社會', '通識校基本素養', '大學導師', '通識跨院基本素養', 'OCW', '品德教育', '語言與溝通-第二外語', '開放隨班附讀', '基本素養-組織管理', '音樂指導(個別指導費)', '專題演講', '遠距課程', '人權教育', '生命教育', '程式相關', '語言與溝通-英文', '媒體資訊判讀', '領域課程-人文與美學', '基本素養-量性推理', '核心通識-藝術與文化', '大型展演', '一般實習', '實驗課程', '核心通識-哲學與心靈', '核心通識-歷史與文明', '智財權課程', '寫作課程', '書報專題討論', '核心通識-倫理與道德思考', '專業服務學習', '領域課程-個人、社會與文化', '大學專題', '基本素養-生命及品格教育', '博雅選修通識', '不支援核心', '領域課程-社會中的科技與自然', '語言與溝通-溝通表達', '語言領域-中文(含寫作)', '性平相關課程', '基本素養-批判思考', '核心通識-社會與經濟', '語言領域-英文', '人文關懷', '社會參與', '領域課程-公民與倫理思考']
CLASS_CONST = {'YN': '護理館', 'YE': '實驗大樓', 'YR': '守仁樓', 'YS': '醫學二館', 'YB': '生醫工程館', 'YX': '知行樓', 'YD': '牙醫館', 'YK': '傳統醫學大樓(甲棟)', 'YT': '教學大樓', 'YM': '醫學館', 'YL': '圖書資源暨研究大樓', 'YA': '活動中心', 'YH': '致和樓', 'YC': '生物醫學大樓', 'AS': '中央研究院', 'PH': '臺北榮民總醫院', 'CH': '台中榮民總醫院', 'KH': '高雄榮民總醫院', 'C': '竹銘館', 'E': '教學大樓', 'LI': '實驗一館', 'BA': '生科實驗館', 'BB': '生科實驗二館', 'BI': '賢齊館', 'EA': '工程一館', 'EB': '工程二館', 'EC': '工程三館', 'ED': '工程四館', 'EE': '工程五館', 'EF': '工程六館', 'M': '管理館', 'MB': '管理二館', 'SA': '科學一館', 'SB': '科學二館', 'SC': '科學三館', 'AC': '學生活動中心', 'A': '綜合一館', 'AB': '綜合一館地下室', 'HA': '人社一館', 'F': '人社二館', 'HB': '人社二館', 'HC': '人社三館', 'CY': '交映樓', 'EO': '田家炳光電大樓', 'EV': '環工館', 'CS': '資訊技術服務中心', 'ES': '電子資訊中心', 'CE': '土木結構實驗室', 'AD': '大禮堂', 'Lib': '浩然圖書資訊中心', 'TA': '會議室', 'TD': '一般教室', 'TC': '演講廳', 'CM': '奇美樓', 'HK': '客家大樓'}

def find(df: pd.DataFrame, condition: condition_lit, condi_args: str| list[str]):
    """擷取資料

    Parameters
    ----------
    df : pd.DataFrame
        總表
    condition : condition_lit
        資料種類
    condi_args : str | list[str]
        資料細項

    Returns
    -------
    pd.DataFrame
    """
    if isinstance(condi_args, str): condi_args = [condi_args]
    match condition:
        case 'time':
            df_temp = df[df['cos_data'].apply(lambda x: any(c_arg in str(x).split(",")[0] for c_arg in condi_args))]
        case "class":
            df_temp = df[df['cos_data'].apply(lambda x: any(c_arg in re.findall(r"([A-Za-z]+)",str(x).split(",")[1]) for c_arg in condi_args))]
        case 'campus':
            df_temp = df[df['cos_data'].apply(lambda x: any(c_arg in str(x).split(",")[2] for c_arg in condi_args))]
        case "type":
            df_temp = df[df['brief'].apply(lambda x: any(c_arg in str(x) for c_arg in condi_args))]
    return df_temp

def main():
    df = pd.read_excel("timetableDate.xlsx")
    df = find(df,'time',["M3","M4","T3","T4","T5","T6",'R1', 'R2', 'R3', 'R4', 'Rn', 'R5', 'R6', 'R7', 'R8', 'R9', 'Ra', 'Rb', 'Rc', 'Rd', 'Fy', 'Fz', 'F1', 'F2'])
    df = find(df,'class',["CS","A"])
    df = find(df, 'type', ["實驗課程","領域課程-人文與美學"])
    df.to_excel("extract.xlsx")
    return df

if __name__ == "__main__":
    print(main())
    pass