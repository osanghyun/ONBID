from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium import webdriver
import json
import re
from ONBID.webpage.common import wait
from ONBID.webpage.common import handle


class MULGUN_GAMJUNG:
    def __init__(self, announce_no):
        self.gamjung: dict = {
            'MNG_NO': "",  # 물건번호
            'ANNOUNCE_NO': announce_no,  # 공고번호
            'GAM_ORGAN': "",  # 감정평가기관
            'GAM_DATE': "",  # 감정일
            'GAM_PRICE': "",  # 감정가
            'LINK': ""  # 파일
        }

    def load_data(self, driver: webdriver.Chrome, button: WebElement) -> None:
        """
        :desc 물건 세부 정보 버튼의 감정평가 데이터 적재.
        :param driver: 크롬 드라이버
        :param button: 물건 세부정보 버튼
        :return:
        """
        handle.button_click(button)

        wait.element_locate(driver, By.ID, "first01")
        main_element: WebElement = driver.find_element(by=By.ID, value="first01")

        if wait.is_element_presence(driver, By.CLASS_NAME, "tab_wrap1.pos_rel"):
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
        else:
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")

        mulgun_number: str = tab_wrap.find_element(
            by=By.CSS_SELECTOR, value="div.finder03 >div > div.txt_top > p.fl.fwb > span:nth-child(2)").text

        self.gamjung['MNG_NO'] = mulgun_number

        try:
            div_elements: list = main_element.find_elements(by=By.CLASS_NAME, value="op_bid_twrap.mt15")

            for category in div_elements:
                category: WebElement
                headline: str = category.find_element(by=By.TAG_NAME, value="h4").text

                if "감정평가정보" in headline:
                    body: WebElement = category.find_element(by=By.ID, value="resultApslList")
                    wait.element_locate(driver=driver, by_type=By.CSS_SELECTOR, locator="tbody#resultApslList > tr")
                    trs: list = body.find_elements(by=By.TAG_NAME, value="tr")

                    for tr in trs:
                        tr: WebElement
                        tds: list = tr.find_elements(by=By.TAG_NAME, value="td")
                        if "없습니다." in tds[0].text:
                            break

                        self.gamjung['GAM_ORGAN'] = tds[0].text
                        self.gamjung['GAM_DATE'] = tds[1].text
                        self.gamjung['GAM_PRICE'] = re.sub(r',', "", tds[2].text)
                        try:
                            self.gamjung['LINK'] = tds[3].find_element(by=By.TAG_NAME,
                                                                       value="a").get_attribute("href")
                        except selenium.common.exceptions.StaleElementReferenceException:
                            print("감정평가서 첨부파일이 없습니다.")
                            self.gamjung['LINK'] = ""
                        except selenium.common.exceptions.NoSuchElementException:
                            print("감정평가서 첨부파일이 없습니다.")
                            self.gamjung['LINK'] = ""

        except selenium.common.exceptions.NoSuchElementException:
            print("감정평가정보 미존재")

    def get_data(self):
        print(json.dumps(self.gamjung, indent=2, ensure_ascii=False))


def get_data(driver: webdriver.Chrome, announce_no: str) -> None:
    """
    물건 세부 정보 버튼이 존재하면 감정평가서 적재하는 함수 호출
    :param driver:
    :param announce_no:
    :return:
    """
    mulgun_detail_button = MULGUN_GAMJUNG(announce_no)

    wait.element_locate(driver, By.CSS_SELECTOR, "#Contents > ul")
    button_tab_table: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > ul")
    button_tabs: list = button_tab_table.find_elements(by=By.TAG_NAME, value="a")

    for button_tab in button_tabs:
        button_tab: WebElement
        title: str = button_tab.text

        if "물건 세부 정보" in title:
            mulgun_detail_button.load_data(driver, button_tab)

    mulgun_detail_button.get_data()