from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium import webdriver
import json
from ONBID.webpage.common import wait, handle
import re


class IPCHAL_HISTORY:
    def __init__(self, mng_no: str, announce_no: str):
        self.ipchal_history = {
            'MNG_NO': mng_no,  # 물건관리번호
            'ANNOUNCE_NO': announce_no,  # 공고 번호
            'HOICHA': "",  # 회차
            'CHASU': "",  # 차수
            'IPCHAL_NO': "",  # 입찰 번호
            'SELL_TYPE': "",  # 처분 방식
            'GAECHAL_YMD': "",  # 개찰 년월일
            'GAECHAL_HM': "",  # 개찰 시분
            'LOW_PRICE': "",  # 최저입찰가
            'RESULT': "",  # 입찰 결과
            'NAK_PRICE': "",  # 낙찰가
            'NAK_PERCENT': "",  # 낙찰가율
            'YU_IPCHALJA': "",  # 유효 입찰자 수
            'MU_IPCHALJA': "",  # 무효 입찰자 수
            'JIPHAENG_YMD': "",  # 집행 완료 년월일
            'JIPHAENG_HM': ""  # 집행 완료 시분
        }

    @staticmethod
    def ipchal_detail(driver: webdriver.Chrome, button: WebElement, dict_history: dict) -> dict:
        """
        입찰 이력 상세보기 버튼 클릭 후 입찰자수, 집행완료일시 정보 적재.
        :param driver: 크롬 드라이버
        :param button: 입찰 이력 상세보기 버튼 WebElement
        :param dict_history: 정보가 적재되는 dictionary
        :return: 정보가 적재된 dictionary
        """
        handle.button_click(button)

        main: list = driver.window_handles

        driver.switch_to.window(main[2])

        wait.element_locate(driver, By.CSS_SELECTOR, "body > div > div.popup_container > table > tbody")

        tbody: WebElement = driver.find_element(By.CSS_SELECTOR, "body > div > div.popup_container > table > tbody")

        trs: list = tbody.find_elements(By.TAG_NAME, "tr")

        for tr in trs:
            tr: WebElement
            ths: list = tr.find_elements(By.TAG_NAME, "th")
            tds: list = tr.find_elements(By.TAG_NAME, "td")
            for i in range(len(ths)):
                head: str = ths[i].text
                body: str = tds[i].text

                if "입찰자수" in head:
                    list_data: list = re.findall(r'[\d]+', body)
                    dict_history['YU_IPCHALJA'] = list_data[0]
                    dict_history['MU_IPCHALJA'] = list_data[0]

                elif "집행완료일시" in head:
                    dict_history['JIPHAENG_YMD'] = re.findall(r'[\d]{4}-[\d]{2}-[\d]{2}', body)[0]
                    dict_history['JIPHAENG_HM'] = re.findall(r'[\d]{2}:[\d]{2}', body)[0]

        driver.close()
        driver.switch_to.window(main[0])

        return dict_history

    def scan_ipchal_table(self, driver: webdriver.Chrome) -> None:
        """
        입찰 이력 테이블을 돌며 상세 보기 탭이 존재하면 상세 보기 정보를 가져오는 함수 호출
        :param driver: 크롬 드라이버
        :return: None
        """
        ipchal_text: str = driver.find_element(by=By.CSS_SELECTOR,
                                               value="#Contents > div.op_bid_twrap.mt10 > div.finder1.pos_rel \
                                               > table > tbody > tr > td").text
        if "없습니다" in ipchal_text:
            return

        tbody: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                value="#Contents > div.op_bid_twrap.mt10\
                                                > div.finder1.pos_rel > table > tbody")
        trs: list = tbody.find_elements(by=By.TAG_NAME, value="tr")

        for tr in trs:
            tr: WebElement
            tds: list = tr.find_elements(by=By.TAG_NAME, value="td")
            dict_history: dict = self.ipchal_history.copy()

            list_data: list = re.split(r'/', tds[0].text)
            dict_history['HOICHA'] = list_data[0]
            dict_history['CHASU'] = list_data[1]

            dict_history['IPCHAL_NO'] = tds[1].text

            dict_history['SELL_TYPE'] = tds[2].text

            list_data = re.split(r' ', tds[3].text)
            dict_history['GAECHAL_YMD'] = list_data[0]
            dict_history['GAECHAL_HM'] = list_data[1]

            str_data: str = re.sub(r'[,원]', "", tds[4].text)
            dict_history['LOW_PRICE'] = str_data

            dict_history['RESULT'] = tds[5].text

            if '-' not in tds[6].text:
                list_data: list = re.split(r'\n', tds[6].text)
                dict_history['NAK_PRICE'] = re.sub(r'[,원]', "", list_data[0])
                dict_history['NAK_PERCENT'] = list_data[1][:-1]

            try:
                button: WebElement = tds[7].find_element(By.TAG_NAME, "a")
                dict_history = self.ipchal_detail(driver, button, dict_history)
            except selenium.common.exceptions.NoSuchElementException:
                print("NO IPCHAL DETAIL")
            except selenium.common.exceptions.StaleElementReferenceException:
                print("NO IPCHAL DETAIL")

            print(json.dumps(dict_history, indent=2, ensure_ascii=False))


def get_data(driver: webdriver.Chrome, announce_no: str) -> None:
    """
    물건 관리 번호 적재 후 입찰 이력 기본 정보와 상세 정보를 적재하는 IPCHAL_HISTORY 클래스 호출
    :param driver: 크롬 드라이버
    :param announce_no: 공고 번호
    :return: None
    """
    if wait.is_element_presence(driver, By.CSS_SELECTOR, "#Contents > div.tab_wrap1.pos_rel"):
        tab_wrap: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                   value="#Contents > div.tab_wrap1.pos_rel")
    else:
        tab_wrap: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                   value="#Contents > div.tab_wrap.pos_rel")

    MNG_NO: str = tab_wrap.find_element(By.CSS_SELECTOR,
                                        "div.finder03 > div > div.txt_top > p.fl.fwb > span:nth-child(2)").text

    ipchal_class = IPCHAL_HISTORY(MNG_NO, announce_no)

    driver.execute_script("""
                    up_window = window.open;
                    window.open = function openWindow(url, blank){
                        up_window(url, "_blank").focus();
                    }""")

    ipchal_class.scan_ipchal_table(driver)