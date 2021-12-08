from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium import webdriver
import json
import re
from ONBID.webpage.common import wait, handle


class MULGUN_AREA:
    def __init__(self, announce_no):
        self.myunjuk: dict = {
            'MNG_NO': "",  # 물건번호
            'ANNOUNCE_NO': announce_no,  # 공고번호
            'JONGBYUL': "",  # 종별
            'JIMOK': "",  # 지목
            'AREA': "",  # 면적
            'PYUNG_AREA': "",  # 평수
            'JIBOON': "",  # 지분
            'BIGO': ""  # 비고
        }

    def load_myunjuk(self, driver: webdriver.Chrome, category: WebElement) -> None:
        """
        :desc 면적 정보 적재
        :param driver: 크롬 드라이버
        :param category: 면적 정보의 상위 WebElement
        :return: None
        """
        if wait.is_element_presence(driver, By.CLASS_NAME, "tab_wrap1.pos_rel"):
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
        else:
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")

        mulgun_number: str = tab_wrap.find_element(
            by=By.CSS_SELECTOR, value="div.finder03 >div > div.txt_top > p.fl.fwb > span:nth-child(2)").text

        self.myunjuk['MNG_NO'] = mulgun_number

        myunjuk_table: WebElement = category.find_element(by=By.ID, value="resultBuildingList")

        if myunjuk_table.is_displayed():
            if "없습니다" not in myunjuk_table.text:
                innerHTML: str = myunjuk_table.get_attribute('innerHTML')
                trPattern = re.compile(r'<tr>[^r]*</tr>')
                trHTML_list: list = trPattern.findall(innerHTML)

                for trHTML in trHTML_list:
                    tdPattern = re.compile(r'<td>[^d]*</td>')
                    tdHTML_list: list = tdPattern.findall(trHTML)

                    erasePattern = re.compile(r'[^tdg<>/&;,㎡ ]+')

                    jong_list: list = erasePattern.findall(tdHTML_list[1])  # 종별(지목)
                    self.myunjuk['JONGBYUL'] = jong_list[0]

                    if len(jong_list) == 2:
                        self.myunjuk['JIMOK'] = jong_list[1]
                    elif len(jong_list) == 3:
                        self.myunjuk['JIMOK'] = jong_list[1] + jong_list[2]

                    myunjuk_list: list = erasePattern.findall(tdHTML_list[2])  # 면적
                    str_data: str = ""
                    for word in myunjuk_list:
                        str_data += word
                    self.myunjuk['AREA'] = re.sub(r'[^\d.]', "", str_data)

                    if not "" == self.myunjuk['AREA']:
                        pyung_area: float = float(self.myunjuk['AREA']) * 0.3025
                        self.myunjuk['PYUNG_AREA'] = pyung_area

                    jibun_list: list = erasePattern.findall(tdHTML_list[3])  # 지분
                    self.myunjuk['JIBOON'] = jibun_list[0]
                    if len(jibun_list) > 1:
                        for i in range(1, len(jibun_list)):
                            self.myunjuk['JIBOON'] += ' ' + jibun_list[i]

                    bigo_list: list = erasePattern.findall(tdHTML_list[4])  # 비고
                    self.myunjuk['BIGO'] = bigo_list[0]
                    if len(bigo_list) > 1:
                        for i in range(1, len(bigo_list)):
                            self.myunjuk['BIGO'] += ' ' + bigo_list[i]
            else:
                print("NO MYUNJUK DATA")

    def load_data(self, driver: webdriver.Chrome, button: WebElement) -> None:
        """
        :desc 물건 세부 정보 버튼 데이터.
        :param driver: 크롬 드라이버
        :param button: 물건 상세정보 탭
        :return: None
        """
        handle.button_click(button)

        wait.element_locate(driver, By.ID, "first01")
        main_element: WebElement = driver.find_element(by=By.ID, value="first01")

        try:
            div_elements: list = main_element.find_elements(by=By.CLASS_NAME, value="op_bid_twrap.cl.mt15")

            for category in div_elements:
                category: WebElement
                headline: str = category.find_element(by=By.TAG_NAME, value="h4").text

                if "면적 정보" in headline:
                    self.load_myunjuk(driver, category)

        except selenium.common.exceptions.NoSuchElementException:
            print("면적정보 데이터 미존재")

    def get_data(self) -> None:
        print(json.dumps(self.myunjuk, indent=2, ensure_ascii=False))


def get_data(driver: webdriver.Chrome, announce_no: str) -> None:
    """
    물건 세부 정보 탭을 클릭 후 면적 정보 적재.
    :param driver: 크롬 드라이버
    :param announce_no: 공고 번호
    :return: None
    """
    area = MULGUN_AREA(announce_no)

    wait.element_locate(driver, By.CSS_SELECTOR, "#Contents > ul")
    button_tab_table: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > ul")
    button_tabs: list = button_tab_table.find_elements(by=By.TAG_NAME, value="a")

    for button_tab in button_tabs:
        button_tab: WebElement
        title: str = button_tab.text

        if "물건 세부 정보" in title:
            area.load_data(driver, button_tab)

    area.get_data()