from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium import webdriver
import json
import sys
import re
from ONBID.webpage.common import wait, handle


class GONGGO_DETAIL:
    def __init__(self, gonggo_basic: dict):
        self.gonggo_detail: dict = {
            'TITLE': gonggo_basic['TITLE'],  # 공고명
            'GONGGO_TYPE': "",  # 공고종류(형식)
            'DATE': gonggo_basic['DATE'],  # 공고일
            'ANNOUNCE_NO': gonggo_basic['ANNOUNCE_NO'],  # 공고번호
            'SELL_TYPE': "",  # 처분방식
            'ASSET': "",  # 자산구분(재산종류)
            'ORGAN_NAME': gonggo_basic['ORGAN_NAME'],  # 공고기관
            'GYUNGJAENG': "",  # 경쟁방식
            'EXE_PART': "",  # 담당부점
            'EXE_NAME': "",  # 담당자 이름
            'EXE_TEL': "",  # 담당자 연락처
            'GONGGO_PAPER': "",  # 공고문 전문
            'START_YMD': gonggo_basic['START_YMD'],  # 입찰시작년도
            'START_HM': gonggo_basic['START_HM'],  # 입찰시작시간
            'END_YMD': gonggo_basic['END_YMD'],  # 입찰마감년도
            'END_HM': gonggo_basic['END_HM'],  # 입찰마감시간
            'GAECHAL_YMD': gonggo_basic['GAECHAL_YMD'],  # 개찰년도
            'GAECHAL_HM': gonggo_basic['GAECHAL_HM'],  # 개찰시간
            'IPCHAL_PERCENT': "",  # 입찰보증금율
            'GAECHAL_LOC': "",  # 개찰장소
            'JUNJA_BOZEUNG': "",  # 전자보증서
            'GONGDONG': "",  # 공동입찰
            'DAELEE': "",  # 대리입찰
            'DONGIL': "",  # 동일 물건 입찰
            'TWO_UCHAL': "",  # 2인 미만 유찰 여부
            'CHASOONWEE': ""  # 차순위 매수신청
        }
        self.file: dict = {
            'FILE_NAME': "",
            'TYPE': "GONGGO",
            'LINK': "",
            'MNG_NO': "",
            'ANNOUNCE_NO': ""
        }

    def load_ipchal(self, driver: webdriver.Chrome) -> None:
        """
        :desc 공고 물건 입찰 정보 적재.
        :param driver: 크롬 드라이버
        :return: None
        """
        if wait.is_element_presence(driver, By.CSS_SELECTOR, "#Contents > ul > li:nth-child(2) > a"):
            ipchal_info_button: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                                 value="#Contents > ul > li:nth-child(2) > a")
            handle.button_click(ipchal_info_button)

        try:
            WebDriverWait(driver, timeout=2, poll_frequency=0.1)\
                .until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#tab_02 > div:nth-child(1) > div")))
        except selenium.common.exceptions.TimeoutException:
            print("공고물건 입찰정보 데이터 미존재")
            driver.close()
            driver.quit()
            sys.exit()

        ipcahl_info_wrap: WebElement = driver.find_element(By.CSS_SELECTOR, "#tab_02 > div:nth-child(1) > div")

        ipchal_info_list: list = ipcahl_info_wrap.find_elements(By.TAG_NAME, "dl")

        self.gonggo_detail['JUNJA_BOZEUNG'] = ipchal_info_list[0].find_element(By.TAG_NAME, "dd").text
        self.gonggo_detail['GONGDONG'] = ipchal_info_list[1].find_element(By.TAG_NAME, "dd").text
        self.gonggo_detail['DAELEE'] = ipchal_info_list[2].find_element(By.TAG_NAME, "dd").text
        self.gonggo_detail['DONGIL'] = ipchal_info_list[3].find_element(By.TAG_NAME, "dd").text
        self.gonggo_detail['TWO_UCHAL'] = ipchal_info_list[4].find_element(By.TAG_NAME, "dd").text
        self.gonggo_detail['CHASOONWEE'] = ipchal_info_list[5].find_element(By.TAG_NAME, "dd").text

        if wait.is_element_presence(driver, By.CSS_SELECTOR, "#tab_02 > div:nth-child(2) > div > table > tbody"):
            tbody: WebElement = driver.find_element(By.CSS_SELECTOR, "#tab_02 > div:nth-child(2) > div > table > tbody")
            tr: WebElement = tbody.find_element(By.TAG_NAME, "tr")

            if "없습니다" in tr.text:
                return

            tds: list = tr.find_elements(By.TAG_NAME, "td")

            self.gonggo_detail['IPCHAL_PERCENT'] = re.sub(r'[^\d]', "", tds[1].text)
            self.gonggo_detail['GAECHAL_LOC'] = tds[4].text

    def load_data(self, driver: webdriver.Chrome) -> None:
        """
        :desc 공고 상세 정보와 공고문 전문 적재.
        :param driver: 크롬 드라이버
        :return: None
        """
        # 공고 테이블
        if wait.is_element_presence(driver, By.CSS_SELECTOR, "#Contents > div.top_wrap2.pos_rel > table > tbody > tr"):
            table: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                    value="#Contents > div.top_wrap2.pos_rel > table")
            tbody: WebElement = table.find_element(by=By.TAG_NAME, value="tbody")
            trs: list = tbody.find_elements(by=By.TAG_NAME, value="tr")

            for tr in trs:
                tr: WebElement
                ths: list = tr.find_elements(by=By.TAG_NAME, value="th")
                tds: list = tr.find_elements(by=By.TAG_NAME, value="td")

                for i in range(len(tds)):
                    header: str = ths[i].text
                    body: str = tds[i].text

                    if '공고종류' in header:
                        self.gonggo_detail['GONGGO_TYPE'] = body

                    elif '처분방식' in header:
                        self.gonggo_detail['SELL_TYPE'] = body

                    elif '자산구분' in header:
                        self.gonggo_detail['ASSET'] = body\

                    elif '경쟁방식' in header:
                        self.gonggo_detail['GYUNGJAENG'] = body

                    elif '담당자정보' in header:
                        list_data: list = re.split(r' \| ', body)
                        self.gonggo_detail['EXE_PART'] = list_data[0]
                        self.gonggo_detail['EXE_NAME'] = list_data[1]
                        self.gonggo_detail['EXE_TEL'] = list_data[2]

        # 공고문 전문
        if wait.is_element_presence(driver, By.CSS_SELECTOR, "#tab_01 > div.op_bid_twrap.mt10 > div > div > div"):
            gonggo_text: str = driver.find_element(by=By.CSS_SELECTOR,
                                                   value="#tab_01 > div.op_bid_twrap.mt10 > div > div > div").text
            self.gonggo_detail['GONGGO_PAPER'] = gonggo_text

    def get_chumbu(self, driver: webdriver.Chrome, announce_no: str) -> None:
        """
        :desc 공고문 첨부파일 적재.
        :param driver: 크롬 드라이버
        :param announce_no: 공고 번호
        :return: None
        """
        if wait.is_element_presence(driver, By.CSS_SELECTOR, "#tab_01 > div.op_bid_twrap.mt15 > div"):
            file_body: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                        value="#tab_01 > div.op_bid_twrap.mt15 > div")
            file_list: list = file_body.find_elements(by=By.TAG_NAME, value="a")

            for file in file_list:
                file: WebElement
                dict_chumbu: dict = self.file.copy()

                text: str = file.text
                href: str = file.get_attribute('href')
                dict_chumbu['FILE_NAME'] = text
                dict_chumbu['LINK'] = href
                dict_chumbu['ANNOUNCE_NO'] = announce_no
                print(json.dumps(dict_chumbu, indent=2, ensure_ascii=False))

    def get_data(self):
        print(json.dumps(self.gonggo_detail, indent=2, ensure_ascii=False))


def get_data(driver: webdriver.Chrome, gonggo_basic: dict) -> None:
    """
    :desc 공고 상세 정보와 공고문 전문, 공고 첨부파일, 공고물건 입찰정보 적재.
    :param driver: 크롬 드라이버
    :param gonggo_basic: 공고 기본 정보
    :return: None
    """
    gonggo = GONGGO_DETAIL(gonggo_basic)

    gonggo.load_data(driver)
    gonggo.load_ipchal(driver)
    gonggo.get_chumbu(driver, gonggo_basic['ANNOUNCE_NO'])
    gonggo.get_data()