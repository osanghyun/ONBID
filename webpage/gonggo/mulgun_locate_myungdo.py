from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium import webdriver
import json
from ONBID.webpage.common import wait, handle


class MULGUN_LOCATE_MYUNGDO:
    def __init__(self, announce_no):
        self.locate_myungdo: dict = {
            'MNG_NO': "",  # 물건번호
            'ANNOUNCE_NO': announce_no,  # 공고번호
            'JIBUN_ADDR': "",  # 지번
            'DORO_ADDR': "",  # 도로명
            'LOCATION': "",  # 위치 및 부근현황
            'USE_HYUN': "",  # 이용현황
            'ETC_ISSUE': "",  # 기타사항
            'EVICTION_RESP': "",  # 명도책임
            'BUDAE': ""  # 부대조건
        }

    def load_data(self, driver: webdriver.Chrome, button: WebElement) -> None:
        """
        :desc 물건 세부 정보 탭안의 위치 및 이용현황 데이터 적재
        :param driver: 크롬 드라이버
        :param button: 물건 세부 정보 탭 WebElement
        :return: None
        """
        if wait.is_element_presence(driver, By.CLASS_NAME, "tab_wrap1.pos_rel"):
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
        else:
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")

        mulgun_number: str = tab_wrap.find_element(
            by=By.CSS_SELECTOR, value="div.finder03 >div > div.txt_top > p.fl.fwb > span:nth-child(2)").text

        self.locate_myungdo['MNG_NO'] = mulgun_number

        handle.button_click(button)

        wait.element_locate(driver, By.ID, "first01")
        main_element: WebElement = driver.find_element(by=By.ID, value="first01")

        try:
            div_elements: list = main_element.find_elements(by=By.CLASS_NAME, value="op_bid_twrap.mt15")

            for category in div_elements:
                category: WebElement
                headline: str = category.find_element(by=By.TAG_NAME, value="h4").text

                if "위치 및 이용현황" in headline:
                    self.locate_myungdo['JIBUN_ADDR'] = category.find_element(by=By.ID, value="jibunadr1").text
                    self.locate_myungdo['DORO_ADDR'] = category.find_element(by=By.ID, value="jibunadr2").text
                    self.locate_myungdo['LOCATION'] = category.find_element(by=By.ID, value="posiEnvPscd").text
                    self.locate_myungdo['USE_HYUN'] = category.find_element(by=By.ID, value="utlzPscd").text
                    self.locate_myungdo['ETC_ISSUE'] = category.find_element(by=By.ID, value="etcDtlCntn").text

                elif "명도이전책임" in headline:
                    self.locate_myungdo['EVICTION_RESP'] = category.find_element(by=By.ID, value="dlvrRsby").text
                    self.locate_myungdo['BUDAE'] = category.find_element(by=By.ID, value="icdlCdtn").text

        except selenium.common.exceptions.NoSuchElementException:
            print("위치 및 이용현황, 명도이전책임 미존재")

    def get_data(self):
        print(json.dumps(self.locate_myungdo, indent=2, ensure_ascii=False))


def get_data(driver: webdriver.Chrome, announce_no: str) -> None:
    """
    :desc 물건 세부 정보 탭이 존재하면 MULGUN_LOCATE_MYUNGDO 클래스를 호출하여 위치 및 이용현황 데이터 적재
    :param driver: 크롬 드라이버
    :param announce_no: 공고 번호
    :return: None
    """
    mulgun_detail_button = MULGUN_LOCATE_MYUNGDO(announce_no)

    wait.element_locate(driver, By.CSS_SELECTOR, "#Contents > ul")
    button_tab_table: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > ul")
    button_tabs: list = button_tab_table.find_elements(by=By.TAG_NAME, value="a")

    for button_tab in button_tabs:
        button_tab: WebElement
        title: str = button_tab.text

        if "물건 세부 정보" in title:
            mulgun_detail_button.load_data(driver, button_tab)

    mulgun_detail_button.get_data()