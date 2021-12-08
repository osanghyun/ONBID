from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium import webdriver
from ONBID.webpage.common import wait, handle
import json
import sys
import re


class IPCHAL:
    def __init__(self, mng_no: str, announce_no: str):
        self.ipchal: dict = {
            'MNG_NO': mng_no,  # 물건 관리 번호
            'ANNOUNCE_NO': announce_no,  # 공고 번호
            'IPCHAL_NO': "",  # 입찰 번호
            'HOICHA': "",  # 회차
            'CHASU': "",  # 차수
            'NAPBU_TYPE': "",  # 대금납부
            'NAPBU_TERM': "",  # 납부기한
        }

    def get_data(self, driver: webdriver.Chrome, button_tab: WebElement) -> None:
        """
        입찰 정보 버튼 클릭 후 회차별 입찰 정보 적재.
        :param driver: 크롬 드라이버
        :param button_tab: 입찰 정보 버튼 WebElement
        :return: None
        """
        handle.button_click(button_tab)

        try:
            WebDriverWait(driver, timeout=4, poll_frequency=0.1). \
                until(EC.visibility_of_element_located((By.ID, "first02")))
        except Exception as e:
            print(str(e))
            sys.exit()

        main_element: WebElement = driver.find_element(by=By.ID, value="first02")

        # 회차별 입찰 정보
        if wait.is_element_presence(driver, By.CSS_SELECTOR, "tbody#resultPbctlList"):
            tbody: WebElement = main_element.find_element(by=By.ID, value="resultPbctlList")

            if tbody.is_displayed():
                try:
                    WebDriverWait(driver=driver, timeout=2, poll_frequency=0.1). \
                        until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody#resultPbctlList > tr")))
                except selenium.common.exceptions.TimeoutException:
                    print("회차별 입찰 정보 Time Out...")
                    driver.close()
                    driver.quit()
                    sys.exit()

                trs = tbody.find_elements(by=By.TAG_NAME, value="tr")
                for tr in trs:
                    if "없습니다" in tr.text:
                        break
                    dict_hweicha: dict = self.ipchal.copy()
                    tds: list = tr.find_elements(by=By.TAG_NAME, value="td")
                    dict_hweicha['IPCHAL_NO'] = tds[0].text
                    p = re.compile(r'[\d]+')
                    m = p.findall(tds[1].text)
                    dict_hweicha['HOICHA'] = m[0]
                    dict_hweicha['CHASU'] = m[1]
                    dict_hweicha['구분'] = tds[2].text
                    dict_hweicha['NAPBU_TYPE'] = tds[3].text.split('\n')[0][:-1]
                    dict_hweicha['NAPBU_TERM'] = tds[3].text.split('\n')[1]
                    print(json.dumps(dict_hweicha, indent=2, ensure_ascii=False))


def get_data(driver: webdriver.Chrome, announce_no: str) -> None:
    """
    :desc 입찰 정보 탭이 존재하면 IPCHAL 클래스를 호출하여 회차별 입찰정보 적재.
    :param driver: 크롬 드라이버
    :param announce_no: 공고 번호
    :return: None
    """
    wait.element_locate(driver, By.CSS_SELECTOR, "#Contents > ul")
    button_tab_table: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > ul")
    button_tabs: list = button_tab_table.find_elements(by=By.TAG_NAME, value="a")

    for button_tab in button_tabs:
        button_tab: WebElement

        title: str = button_tab.text
        if "입찰 정보" in title:
            if wait.is_element_presence(driver, By.CLASS_NAME, "tab_wrap1.pos_rel"):
                tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
            else:
                tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")

            mulgun_number: str = tab_wrap.find_element(
                by=By.CSS_SELECTOR, value="div.finder03 >div > div.txt_top > p.fl.fwb > span:nth-child(2)").text

            ipchal = IPCHAL(mulgun_number, announce_no)
            ipchal.get_data(driver, button_tab)