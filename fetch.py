from io import StringIO
from time import sleep
from typing import Literal, Union, get_args
import pandas as pd
import requests
from azustock.core.quote_opti import process_time

def to_txt(text, file_path: str= "output.txt", encoding: str='utf-8') -> None:
    """
    Warning! we use "print" to save
    """
    with open(file_path, 'w', encoding=encoding, errors='replace') as f:
        print(text, file=f)

class fetcher:
    FetchTimeType = Literal['y', 'z', '1', '2', '3', '4', 'n', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd']
    FetchDateType = Literal['M', 'T', 'W', 'R', 'F', 'S', 'U']
    Fetchcostype_dic = {'OCW': '28', '遠距課程': '4', '服務學習': '7', '智財權課程': '8', '性平相關課程': '9', '英文授課': '13', '通識校基本素養': '15', '通識跨院 基本素養': '16', '通識核心課程': '17', '一般實習': '26', '語言領域-中文(含寫作)': '29', '語言領域-英文': '30', '核心通識-哲學與心靈': '31', '核心通識-歷史與文明': '32', '核心通識-社會與經濟': '33', '核心通識-倫理與道德思考': '34', '核心通識-科技與社會': '35', '核心通識-藝術與文化': '36', '博雅選修通識': '37', '基本素養-批判思考': '44', '基本素養-量性推理': '45', '基本素養-組織管理': '46', '基本素養-生命及品格教育': '47', '領域課程-人文與美學': '48', '領域課程-個人、社會與文化': '49', '領域課程-公民與倫理思考': '50', '領域課程-社會中的科技與自然': '51', '語言與溝通-英文': '52', '語言與溝通-國家語言': '53', '語言與溝通-第二外語': '54', '語言與溝通-溝通表達': '55', '語言與溝通-寫作課程': '56', '跨校區課程': '57', '程式相關': '58', '實驗課程': '59', '臨床實習': '60', '大型展演': '61', '專題演講': '62', '書報專題討論': '63', '大學專 題': '64', '大學導師': '65', '臨床導師': '66', '音樂指導(個別指導費)': '67', '音樂分組': '68', '寫作課程': '69', '校際合開課程': '70', '開放隨班附讀': '71', '不支援核心': '73', '社會參與': '74', '媒體資訊判讀': '75', '基礎服務學習': '76', '專業服務學習': '77', '人文關懷': '78', '人權教育': '79', '品德教育': '80', '生命教育': '81'}

    def __init__(self):
        self.__time_dic = Literal['My', 'Mz', 'M1', 'M2', 'M3', 'M4', 'Mn', 'M5', 'M6', 'M7', 'M8', 'M9', 'Ma', 'Mb', 'Mc', 'Md', 'Ty', 'Tz', 'T1', 'T2', 'T3', 'T4', 'Tn', 'T5', 'T6', 'T7', 'T8', 'T9', 'Ta', 'Tb', 'Tc', 'Td', 'Wy', 'Wz', 'W1', 'W2', 'W3', 'W4', 'Wn', 'W5', 'W6', 'W7', 'W8', 'W9', 'Wa', 'Wb', 'Wc', 'Wd', 'Ry', 'Rz', 'R1', 'R2', 'R3', 'R4', 'Rn', 'R5', 'R6', 'R7', 'R8', 'R9', 'Ra', 'Rb', 'Rc', 'Rd', 'Fy', 'Fz', 'F1', 'F2', 'F3', 'F4', 'Fn', 'F5', 'F6', 'F7', 'F8', 'F9', 'Fa', 'Fb', 'Fc', 'Fd', 'Sy', 'Sz', 'S1', 'S2', 'S3', 'S4', 'Sn', 'S5', 'S6', 'S7', 'S8', 'S9', 'Sa', 'Sb', 'Sc', 'Sd', 'Uy', 'Uz', 'U1', 'U2', 'U3', 'U4', 'Un', 'U5', 'U6', 'U7', 'U8', 'U9', 'Ua', 'Ub', 'Uc', 'Ud']
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/111.25 (KHTML, like Gecko) Chrome/99.0.2345.81 Safari/123.36'}

    def __combine_time(self, time_l: list[str] | None = None, date_l: list[str] | None = None) -> list[str]:
        #輸入初處理
        if time_l is None:
            time_l = list(get_args(fetcher.FetchTimeType))
        elif not isinstance(time_l, (list, str)):
            raise TypeError("'time_l' must be a 'list' or 'str'.")
        if date_l is None:
            date_l = list(get_args(fetcher.FetchDateType))
        elif not isinstance(date_l, (list, str)):
            raise TypeError("'date_l' must be a 'list' or 'str'.")
        
        ret_l = []
        for d in date_l:
            for t in time_l:
                ret_l.append(d + t)
        return ret_l

    @process_time()
    def fetch(self,
              costype: dict | None = None,
              full_file_name: str = 'timetable.xlsx') -> pd.DataFrame:
        
        url = "https://timetable.nycu.edu.tw"
        
        params = {
        "r": "main/get_cos_list"
        }
        if costype is None:
            costype = fetcher.Fetchcostype_dic
        elif not isinstance(costype, (dict)):
            raise TypeError("'costype' must be a 'dict'.")
        run_dic = costype
        df_all = pd.DataFrame()
        process_bar = [0,len(run_dic)]
        for key in run_dic:
            print(f"\rFetch {key}: {process_bar[0]}/{process_bar[1]}            ",end="")
            process_bar[0] += 1

            payload = {"m_acy": 113,
            "m_sem": 1,
            "m_acyend": 113,
            "m_semend": 1,
            "m_dep_uid": "**",
            "m_group": "**",
            "m_grade": "**",
            "m_class": "**",
            "m_option": "costype",
            "m_crsname": "**",
            "m_teaname": "**",
            "m_cos_id": "**",
            "m_cos_code": "**",
            "m_crstime": "**",
            "m_crsoutline": "**",
            "m_costype": run_dic[key],
            "m_selcampus": "**"}

            res = requests.post(url,params=params, data=payload,headers=self.headers)
            res.text
            js = res.json()
            dic_data = {}
            df_brief = pd.DataFrame()
            
            for js_key in js:
                
                for sub_key in js[js_key]:
                    #print(sub_key)
                    try:
                        int(sub_key)
                        sub_js = js[js_key][sub_key]
                        dic_data = dic_data | sub_js
                        
                    except ValueError:
                        if sub_key == 'brief':
                            for dic_key in js[js_key]["brief"]:
                                d = js[js_key]["brief"][dic_key]
                                for hi in d:
                                    result = {"code": dic_key, "data": d[hi]['brief']}
                                    df_brief = pd.concat([df_brief, pd.DataFrame(result, index=[0])], ignore_index=True)

                df_raw = pd.DataFrame(dic_data)
                df = df_raw.T
                df['課程屬性'] = [""]*df.shape[0]
                df['屬性'] = [key]*df.shape[0]
                df.reset_index(inplace=True)
                for i in df.index:
                    try:
                        df.loc[i, '課程屬性'] = df_brief.loc[df_brief['code'] == df.loc[i, 'index'], "data"].values[0]
                    except IndexError:
                        df.loc[i, '課程屬性'] = None
                df_all = pd.concat([df_all, df])
        print(f"\rFetch {key}: {process_bar[0]}/{process_bar[1]}            ",end="")
        df_all.drop_duplicates(subset=['index','cos_id','cos_code'],inplace=True,ignore_index=True)
        typ = full_file_name.split('.')[-1]
        match typ:
            case 'xlsx':
                df_all.to_excel(f"{full_file_name}")
            case _ as e:
                raise ValueError(f"'{e}' is not a valid type")
        print(f"\rFetch 完成: {process_bar[1]}/{process_bar[1]}            ")
        return df_all

if __name__ == "__main__":
    f = fetcher()
    f.fetch()
    pass