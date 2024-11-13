from io import StringIO
from time import sleep
from typing import Literal, Union, get_args
import pandas as pd
import requests

def to_txt(text, file_path: str= "output.txt", encoding: str='utf-8') -> None:
    """
    Warning! we use "print" to save
    """
    with open(file_path, 'w', encoding=encoding, errors='replace') as f:
        print(text, file=f)

class fetcher:
    FetchTimeType = Literal['y', 'z', '1', '2', '3', '4', 'n', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd']
    FetchDateType = Literal['M', 'T', 'W', 'R', 'F', 'S', 'U']

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

    def fetch(self,
              time_l: Union['fetcher.FetchTimeType', list[str], None] = None,
              date_l: Union['fetcher.FetchDateType', list[str], None] = None,
              full_file_name: str = 'timetable.csv') -> pd.DataFrame:
        
        url = "https://timetable.nycu.edu.tw"
        
        params = {
        "r": "main/get_cos_list"
        }
        combine_l = self.__combine_time(time_l, date_l)
        run_l = [combine_l[i:i+16] for i in range(0, len(combine_l), 16)]
        df_all = pd.DataFrame()
        for m_crstimes in run_l:
            m_crstime = ",".join(str(i) for i in m_crstimes)

            payload = {"m_acy": 113,
            "m_sem": 1,
            "m_acyend": 113,
            "m_semend": 1,
            "m_dep_uid": "**",
            "m_group": "**",
            "m_grade": "**",
            "m_class": "**",
            "m_option": "crstime",
            "m_crsname": "**",
            "m_teaname": "**",
            "m_cos_id": "**",
            "m_cos_code": "**",
            "m_crstime": m_crstime,
            "m_crsoutline": "**",
            "m_costype": "**",
            "m_selcampus": "**"}

            res = requests.post(url,params=params, data=payload,headers=self.headers)
            js = res.json()
            dic_data = {}
            i = 0
            for key in js:
                for sub_key in js[key]:
                    try:
                        int(sub_key)
                        sub_js = js[key][sub_key]
                        dic_data = dic_data | sub_js
                    except ValueError:
                        pass
            df_raw = pd.DataFrame(dic_data)
            df = df_raw.T
            df_all = pd.concat([df_all, df])
        
        typ = full_file_name.split('.')[-1]
        match typ:
            case 'xlsx':
                df_all.to_excel(f"{full_file_name}")
            case 'csv':
                df_all.to_csv(f"{full_file_name}")
            case _ as e:
                raise ValueError(f"'{e}' is not a valid type")
        return df_all

if __name__ == "__main__":
    f = fetcher()
    f.fetch()
    pass