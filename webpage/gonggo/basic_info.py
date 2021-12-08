from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import re


class GONGGO_BASIC:
    def __init__(self):
        self.gonggo_basic: dict = {
            'ANNOUNCE_NO': "",  # 공고번호
            'TITLE': "",  # 공고명
            'TAG': [],  # 태그
            'ORGAN_NAME': "",  # 기관명
            'EXE_PART': "",  # 담당부점
            'DATE': "",  # 공고일자(년월일)
            'START_YMD': "",  # 입찰시작일시 (년월일)
            'START_HM': "",  # 입찰시작일시 (시분)
            'END_YMD': "",  # 입찰마감일시 (년월일)
            'END_HM': "",  # 입찰마감일시 (시분)
            'GAECHAL_YMD': "",  # 개찰일시 (년월일)
            'GAECHAL_HM': ""  # 개찰일시 (시분)
        }

    def load_data(self, driver: webdriver.Chrome, gonggo_index: int) -> None:
        """
        :desc 데이터 적재
        :param driver: 크롬 드라이버
        :param gonggo_index: 테이블에서의 위치
        :return: None
        """
        tr: WebElement = driver.find_element(By.CSS_SELECTOR, "#Contents > table > tbody > tr:nth-child(" +
                                             f"{gonggo_index + 1})")

        tds: list = tr.find_elements(By.TAG_NAME, "td")

        self.gonggo_basic['ANNOUNCE_NO'] = tds[0].find_element(By.TAG_NAME, "dt").text
        self.gonggo_basic['TITLE'] = tds[0].find_element(By.TAG_NAME, "dd").text
        badge: WebElement = tds[0].find_element(By.CSS_SELECTOR, "dl > dd.badge_wrap.mt5")
        self.gonggo_basic['TAG'] = re.split(r'\n', badge.text)

        list_data: list = re.split(r'\n', tds[1].text)
        self.gonggo_basic['ORGAN_NAME'] = list_data[0]
        self.gonggo_basic['EXE_PART'] = list_data[1][1:-1]

        self.gonggo_basic['DATE'] = tds[2].text

        YMD: list = re.findall(r'[\d]{4}-[\d]{2}-[\d]{2}', tds[3].text)
        HM: list = re.findall(r'[\d]{2}:[\d]{2}', tds[3].text)
        self.gonggo_basic['START_YMD'] = YMD[0]
        self.gonggo_basic['START_HM'] = HM[0]
        self.gonggo_basic['END_YMD'] = YMD[1]
        self.gonggo_basic['END_HM'] = HM[1]

        list_data: list = re.split(r' ', tds[4].text)
        self.gonggo_basic['GAECHAL_YMD'] = list_data[0]
        self.gonggo_basic['GAECHAL_HM'] = list_data[1]

    def get_data(self) -> dict:
        """
        :desc 클래스의 dict형 변수 반환.
        :return: 공고 요약정보
        """
        print(json.dumps(self.gonggo_basic, indent=2, ensure_ascii=False))

        return self.gonggo_basic


def get_data(driver: webdriver.Chrome, gonggo_index: int) -> dict:
    """
    :desc GONGGO_BASIC 클래스의 dict형 변수에 데이터를 적재 후 반환
    :param driver: 크롬 드라이버
    :param gonggo_index: 테이블에서의 위치
    :return: 공고 요약정보
    """
    gonggo = GONGGO_BASIC()

    gonggo.load_data(driver, gonggo_index)

    gonggo_basic: dict = gonggo.get_data()

    return gonggo_basic