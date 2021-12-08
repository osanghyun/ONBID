from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import sys
import re
from ONBID.webpage.common import wait


class MULGUN_DETAIL:
    def __init__(self, announce_no: str):
        self.detail: dict = {
            'MNG_NO': "",  # 물건번호
            'MULGUN_NAME': "",  # 물건명
            'ANNOUNCE_NO': announce_no,  # 공고번호
            'CATEGORY': "",  # 카테고리
            'SUB_CATEGORY': "",  # 부카테고리
            'STATE': "",  # 물건상태
            'GYUNGJAENG': "",  # 경쟁방식
            'IPCHAL_TYPE': "",  # 입찰방식
            'READ_CNT': "",  # 조회수
            'HOICHA': "",  # 회차
            'CHASU': "",  # 차수
            'YUCHAL_CNT': "",  # 유찰횟수
            'LOW_PRICE': "",  # 최저입찰가
            'JONGGI_DATE': "",  # 배분요구종기
            'FIRST_GONGGO': "",  # 최초 공고 일자
            'TAG': []  # 태그,
        }

    def load_data(self, driver: webdriver.Chrome) -> None:
        """
        물건 세부 정보 적재.
        :param driver: 크롬 드라이버
        :return: None
        """
        if wait.is_element_presence(driver, By.CLASS_NAME, "tab_wrap1.pos_rel"):
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
        else:
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")

        mulgun_number: str = tab_wrap.find_element(
            by=By.CSS_SELECTOR, value="div.finder03 >div > div.txt_top > p.fl.fwb > span:nth-child(2)").text

        self.detail['MNG_NO'] = mulgun_number

        fr = tab_wrap.find_element(by=By.CSS_SELECTOR, value="div.finder03 > div > div.txt_top > p.fr")

        spans = fr.find_elements(by=By.TAG_NAME, value="span")

        if len(spans) != 3:
            print("물건상태, 공고일자, 조회수 데이터가 없습니다.")
            sys.exit()

        self.detail['STATE'] = spans[0].find_element(by=By.TAG_NAME, value="em").text
        self.detail['READ_CNT'] = spans[2].find_element(by=By.TAG_NAME, value="em").text

        # 중분류, 소분류, 물건이름
        cl_mt10 = driver.find_element(by=By.CLASS_NAME, value="cl.mt10")
        category_text: str = cl_mt10.find_element(by=By.TAG_NAME, value="p").text
        m: list = re.split(r' / ', category_text[1:-1])
        self.detail['CATEGORY'] = m[0]
        self.detail['SUB_CATEGORY'] = m[1]

        name_text: str = cl_mt10.find_element(by=By.TAG_NAME, value="strong").text
        self.detail['MULGUN_NAME'] = name_text

        # 태그
        badge_wrap = driver.find_element(by=By.CLASS_NAME, value="badge_wrap.mt10")
        badges = badge_wrap.find_elements(by=By.TAG_NAME, value="em")
        badge_list: list = []

        for badge in badges:
            badge_list.append(badge.text)

        self.detail['TAG'] = badge_list

        # 처분방식, 자산구분, 용도, 토지면적, 건물면적, 감정평가금액, 입찰방식, 입찰, 개찰, 회차, 차수, 유찰횟수, 배분요구종기, 최초공고일자, 공매대행의뢰

        body = driver.find_element(by=By.CSS_SELECTOR,
                                   value="#Contents > div.form_wrap.mt20.mb10 > div.check_wrap.fr > table > tbody")

        trs = body.find_elements(by=By.TAG_NAME, value="tr")

        for tr in trs:
            head_line_text: str = tr.find_element(by=By.TAG_NAME, value="th").text
            table_data: str = tr.find_element(by=By.TAG_NAME, value="td").text

            if "입찰방식" in head_line_text:
                m: list = re.split(r' / ', table_data)
                self.detail['GYUNGJAENG'] = m[0]
                self.detail['IPCHAL_TYPE'] = m[1]
                continue

            elif "면적" in head_line_text:
                list_data: list = re.findall(r'[가-힣]+', table_data)
                myunjuk_data: list = re.split(r' / ', table_data)
                for i in range(len(list_data)):
                    i: int
                    str_data: str = re.sub(r'[^\d.]', "", myunjuk_data[i])
                    if str_data == "":
                        self.detail[f'{list_data[i]}면적'] = 0
                    else:
                        self.detail[f'{list_data[i]}면적'] = float(str_data)
                    self.detail[f'{list_data[i]}평수'] = self.detail[f'{list_data[i]}면적'] * 0.3025

            elif "입찰기간" in head_line_text:
                m: list = re.findall(r'[\d]+/[\d]+', table_data)
                data: list = m[0].split('/')
                self.detail['HOICHA'] = data[0]
                self.detail['CHASU'] = data[1]
                continue

            elif "유찰횟수" in head_line_text:
                str_data: str = re.sub(r'[\D]', "", table_data)
                self.detail['YUCHAL_CNT'] = str_data
                continue

            elif "배분요구종기" in head_line_text:
                self.detail['JONGGI_DATE'] = table_data
                continue

            elif "최초공고일자" in head_line_text:
                self.detail['FIRST_GONGGO'] = table_data
                continue

            bid_price_text: str = driver.find_element(by=By.CSS_SELECTOR,
                                                      value="#Contents > div.form_wrap.mt20.mb10 > \
                                                      div.check_wrap.fr > dl > dd > em").text
            bid_price: str = re.sub(r'\D', "", bid_price_text)
            self.detail['LOW_PRICE'] = bid_price

    def get_data(self):
        print(json.dumps(self.detail, indent=2, ensure_ascii=False))


def get_data(driver: webdriver.Chrome, gonggo_nm: str) -> None:
    """
    물건 세부 정보 데이터 저장.
    :param driver:
    :param gonggo_nm:
    :return:
    """
    detatil = MULGUN_DETAIL(gonggo_nm)
    detatil.load_data(driver)
    # todo detatil.get_data()