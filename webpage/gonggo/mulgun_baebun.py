from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium import webdriver
import json
import re
from ONBID.webpage.common import wait, handle


class MULGUN_BAEBUN:
    def __init__(self, announce_no: str):
        self.kwonlee: dict = {
            'MNG_NO': "",  # 물건번호
            'ANNOUNCE_NO': announce_no,  # 공고번호
            'TYPE': "",  # 권리종류
            'CHAEGWONJA': "",  # 권리자명 (채권자명)
            'SET_DATE': "",  # 설정일자
            'SET_PRICE': "",  # 설정금액
            'BAEBUN_PRICE': "",  # 배분요구일
            'BAEBUN_DATE': "",  # 배분요구액 (배분요구채권액)
            'MALSO': "",  # 말소가능여부
            'ETC': ""  # 기타
        }

    def load_kwonlee(self, driver: webdriver.Chrome, main_element: WebElement) -> None:
        """
        :desc 권리 분석 기초 정보의 배분요구 및 채권신고현황 정보 적재 (압류재산)
        :param driver: 크롬 드라이버
        :param main_element: 압류재산 정보 탭을 감싸는 WebElement
        :return: None
        """
        if wait.is_element_presence(driver, By.CSS_SELECTOR, "tbody#resultShrImfoList"):
            body: WebElement = main_element.find_element(by=By.ID, value="resultShrImfoList")

            try:
                WebDriverWait(driver, timeout=2, poll_frequency=0.1). \
                    until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody#resultShrImfoList > tr")))
            except selenium.common.exceptions.TimeoutException:
                print("권리분석 기초정보 Time Out...")  # 7일전엔 안보임
                return

            trs: list = body.find_elements(by=By.TAG_NAME, value="tr")

            for tr in trs:
                tr: WebElement
                if "없습니다" in tr.text:
                    break
                tds: list = tr.find_elements(by=By.TAG_NAME, value="td")
                self.kwonlee['TYPE'] = tds[1].text
                self.kwonlee['CHAEGWONJA'] = tds[2].text
                self.kwonlee['SET_DATE'] = tds[3].text
                self.kwonlee['SET_PRICE'] = re.sub(r',', "", tds[4].text)
                self.kwonlee['BAEBUN_PRICE'] = tds[5].text
                self.kwonlee['BAEBUN_DATE'] = re.sub(r',', "", tds[6].text)
                self.kwonlee['MALSO'] = tds[7].text
                self.kwonlee['ETC'] = tds[8].text

                self.get_data()

    def load_data(self, driver: webdriver.Chrome, button: WebElement) -> None:
        """
        :desc 물건관리번호를 저장하고 압류재산 정보 탭 클릭 후 권리분석 기초정보 존재 여부 체크
        :param driver: 크롬 드라이버
        :param button: 압류재산 정보 탭
        :return: None
        """
        if wait.is_element_presence(driver, By.CLASS_NAME, "tab_wrap1.pos_rel"):
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
        else:
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")

        mulgun_number: str = tab_wrap.find_element(
            by=By.CSS_SELECTOR, value="div.finder03 >div > div.txt_top > p.fl.fwb > span:nth-child(2)").text

        self.kwonlee['MNG_NO'] = mulgun_number

        handle.button_click(button)

        wait.element_locate(driver, By.ID, "first11")
        main_element: WebElement = driver.find_element(by=By.ID, value="first11")

        if wait.is_element_presence(driver, By.CSS_SELECTOR, "tbody#resultShrImfoList"):
            self.load_kwonlee(driver, main_element)

    def get_data(self):
        print(json.dumps(self.kwonlee, indent=2, ensure_ascii=False))


def get_data(driver: webdriver.Chrome, announce_no: str) -> None:
    """
    :desc 배분 클래스를 생성하고 압류재산 정보 탭으로 이동
    :param driver: 크롬 드라이버
    :param announce_no: 공고 번호
    :return: None
    """
    baebun = MULGUN_BAEBUN(announce_no)

    wait.element_locate(driver, By.CSS_SELECTOR, "#Contents > ul")
    button_tab_table: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > ul")
    button_tabs: list = button_tab_table.find_elements(by=By.TAG_NAME, value="a")

    for button_tab in button_tabs:
        button_tab: WebElement
        title: str = button_tab.text

        if "압류재산 정보" in title:
            baebun.load_data(driver, button_tab)