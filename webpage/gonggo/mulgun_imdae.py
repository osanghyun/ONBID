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


class MULGUN_IMDAE:
    def __init__(self, announce_no: str):
        self.imdae: dict = {
            'MNG_NO': "",  # 물건관리번호
            'ANNOUNCE_NO': announce_no,  # 공고번호
            'IMCHA_EXP': "",  # 임대차내용
            'IMCHAIN': "",  # 이름
            'IMCHA_PRICE': "",  # 보증금
            'CHAIM': "",  # 차임(월세)
            'EXC_PRICE': "",  # 환산보증금
            'DECISION_DATE': "",  # 확정(설정)일
            'REG_DATE': ""  # 전입일
        }

    def load_imdae(self, driver: webdriver.Chrome, main_element: WebElement) -> None:
        """
        :desc 임대차 정보 class의 dict형 인스턴스에 적재.
        :param driver: 크롬 드라이버
        :param main_element: 임대차 정보 테이블 WebElement
        :return: None
        """
        body: WebElement = main_element.find_element(by=By.ID, value="resultLeasImfoList")

        try:
            WebDriverWait(driver, timeout=2, poll_frequency=0.1). \
                until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody#resultLeasImfoList > tr > td")))
        except selenium.common.exceptions.TimeoutException:
            print("임대차 정보(감정평가서 및 신고된 임대차 기준) Time Out...")
            driver.close()
            driver.quit()
            sys.exit()

        trs: list = body.find_elements(by=By.TAG_NAME, value="tr")

        for tr in trs:
            tr: WebElement
            if "없습니다" in tr.text:
                break
            tds: list = tr.find_elements(by=By.TAG_NAME, value="td")
            self.imdae['IMCHA_EXP'] = tds[0].text
            self.imdae['IMCHAIN'] = tds[1].text
            self.imdae['IMCHA_PRICE'] = re.sub(r',', "", tds[2].text)
            self.imdae['CHAIM'] = tds[3].text
            self.imdae['EXC_PRICE'] = tds[4].text
            self.imdae['DECISION_DATE'] = tds[5].text
            self.imdae['REG_DATE'] = tds[6].text

            self.get_data()

    def load_data(self, driver: webdriver.Chrome, button: WebElement) -> None:
        """
        :desc 물건 관리 번호 dict에 적재, 압류재산 정보 탭 클릭 후 임대차 정보 크롤링 method 호출
        :param driver: 크롬 드라이버
        :param button: 압류 재산 정보 탭 WebElement
        :return: None
        """
        if wait.is_element_presence(driver, By.CLASS_NAME, "tab_wrap1.pos_rel"):
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
        else:
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")

        mulgun_number: str = tab_wrap.find_element(
            by=By.CSS_SELECTOR, value="div.finder03 >div > div.txt_top > p.fl.fwb > span:nth-child(2)").text

        self.imdae['MNG_NO'] = mulgun_number

        handle.button_click(button)

        wait.element_locate(driver, By.ID, "first11")
        main_element: WebElement = driver.find_element(by=By.ID, value="first11")

        if wait.is_element_presence(driver, By.CSS_SELECTOR, "tbody#resultLeasImfoList"):
            self.load_imdae(driver, main_element)

    def get_data(self):
        print(json.dumps(self.imdae, indent=2, ensure_ascii=False))


def get_data(driver: webdriver.Chrome, announce_no: str) -> None:
    """
    :desc 압류재산 정보 탭이 존재하면 임대차 정보를 적재하는 MULGUN_IMDAE 클래스에 데이터 적재.
    :param driver: 크롬 드라이버
    :param announce_no: 공고 번호
    :return: None
    """
    apryu_button = MULGUN_IMDAE(announce_no)

    wait.element_locate(driver, By.CSS_SELECTOR, "#Contents > ul")
    button_tab_table: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > ul")
    button_tabs: list = button_tab_table.find_elements(by=By.TAG_NAME, value="a")

    for button_tab in button_tabs:
        button_tab: WebElement
        title: str = button_tab.text

        if "압류재산 정보" in title:
            apryu_button.load_data(driver, button_tab)