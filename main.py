'''
main.py

描述
-------------------------------------------------
這個專案是為了陽明交通大學113學年度第一學期計算機概論而做的作業。
功能是讓選課過程更加輕鬆愉快。

作者
-------------------------------------------------
Salmoon Sake
在此感謝 曾宗宣 的協助，建議將其改為更易使用的Context Maneger

版本資訊
-------------------------------------------------
v1.1
'''
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class Searcher:
    '''
    該類的功能是負責進行網路爬蟲，彙整資料並提交
    '''
    def __init__(self) -> None:
        pass

    def __activate_driver(self) -> None:
        '''
        啟動瀏覽器並設置相關參數
        '''

        #確認是否需要下載driver
        service = Service(ChromeDriverManager().install())

        #設置為無頭模式(不顯示瀏覽器GUI)
        options = Options()
        options.add_argument("--headless")

        #建立chrome driver 實例(因為不清楚其他瀏覽器是否能夠正常瀏覽學校課表)
        self.driver = webdriver.Chrome(service=service,options=options)

        #建立waiter，設定等待上限為10秒，否則載後續處理會引發Timeout
        self.wait = WebDriverWait(self.driver, 10)

    def __goto_url(self,url:str) -> None:
        '''
        前往指定的網頁
        '''
        try:
            self.driver.get(url)
        except Exception as e:
            print("發生未知的錯誤，請確認網路是否正常後再重試")
            raise e

    def get_courses(self,time_slot:str) -> dict[tuple]:
        '''
        獲取本學年度某時段的課程資訊
        '''

        #校驗使用者輸入
        if len(time_slot) > 2:
            raise Exception("錯誤的時段代碼")
        
        if time_slot[0] not in "MTWRFSU":
            raise Exception("不存在的日期代碼")
        
        if time_slot[1] not in "yz1234n56789abcd":
            raise Exception("不存在的時段代碼")

        self.__goto_url(self.url)

        #設置為陽明校區
        chkCampus = self.wait.until(EC.visibility_of_element_located((By.ID, "chkCampus")))
        chkCampus.click()
        ym_campus_chk = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='selcampus' and @value='YM']")))
        ym_campus_chk.click()
        
        #設置為通識課
        fType = self.wait.until(EC.visibility_of_element_located((By.ID, "fType")))
        select = Select(fType)
        select.select_by_index(2)#第[2]個選項是學士班共同課程

        #設置時段
        chkOption = self.wait.until(EC.visibility_of_element_located((By.ID, "chkOption")))
        chkOption.click()
        choose_time = self.wait.until(EC.visibility_of_element_located((By.ID, "choose_time")))
        choose_time.click()
        class_time_chk = self.wait.until(EC.visibility_of_element_located((By.NAME, f"daytime_{time_slot}")))
        class_time_chk.click()
        jqi_state0_buttonOk = self.wait.until(EC.visibility_of_element_located((By.NAME, "jqi_state0_buttonOk")))
        jqi_state0_buttonOk.click()

        #因為學校課表智障、低能的設計，當選擇"特定條件"時，上面的設定會跑掉，要重新勾選
        chkDep = self.wait.until(EC.visibility_of_element_located((By.ID, "chkDep")))
        chkDep.click()

        #按下搜尋按鈕
        crstime_search = self.wait.until(EC.visibility_of_element_located((By.ID, "crstime_search")))
        crstime_search.click()
        succeed = False

        #從網頁中篩選出課程列表物件
        sleep(2)
        try:
            td_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@name="cos_name"]')))
            #建立儲存課程的字典
            courses = dict()

            #遞迴所有找到的課程，並將資訊填入上述字典
            for td_element in td_elements:

                course_name = td_element.text.split("\n")[0]

                #span物件(課程類別)也採用遞迴的方法讀取/寫入
                span_elements = td_element.find_elements(By.TAG_NAME,"span")

                course_properties = list()
                for span_element in span_elements:
                    course_properties.append(span_element.text)
            
                #寫入字典
                courses[course_name] = tuple(course_properties)
            succeed = True

        except  TimeoutException as e:
            ...

        #回復設定
        choose_time.click()
        class_time_chk = self.wait.until(EC.visibility_of_element_located((By.NAME, f"daytime_{time_slot}")))
        class_time_chk.click()
        jqi_state0_buttonOk = self.wait.until(EC.visibility_of_element_located((By.NAME, "jqi_state0_buttonOk")))
        jqi_state0_buttonOk.click()
        chkOption = self.wait.until(EC.element_to_be_clickable((By.ID, "chkOption")))
        sleep(1)
        chkOption.click()
        ym_campus_chk.click()
        chkCampus.click()

        if succeed:
            return courses
        
        return None
    
    def __enter__(self):
        #陽明課程時間表的網頁
        url = "https://timetable.nycu.edu.tw/?flang=zh-tw"
        self.__activate_driver()
        self.__goto_url(url)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        '''
        關閉driver
        '''
        self.driver.quit()

def main():
    with Searcher() as searcher:
        l = ["M5","T5","W5","R5","F5"]
        try:
            for i in l:
                print(searcher.get_courses(i))
            
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()