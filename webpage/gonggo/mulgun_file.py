from selenium.webdriver.common.by import By
from selenium import webdriver
from ONBID.webpage.common import handle
import json
from ONBID.webpage.common import wait


class MULGUN_FILE:
    def __init__(self, announce_no):
        self.file: dict = {
            'TYPE': "",  # 파일 유형
            'LINK': "",  # 링크
            'MNG_NO': "",  # 물건관리번호
            'ANNOUNCE_NO': announce_no  # 공고번호
        }

    def get_data(self) -> None:
        print(json.dumps(self.file, indent=2, ensure_ascii=False))

    def load_photo(self, driver: webdriver.Chrome) -> None:
        """
        :desc 사진 버튼 클릭 후 사진 정보 적재
        :param driver: 크롬 드라이버
        :return: None
        """
        wait.element_locate(driver, By.CLASS_NAME, "visual_inner")
        visual_inner = driver.find_element(by=By.CLASS_NAME, value="visual_inner")

        btn_vway = visual_inner.find_element(by=By.CLASS_NAME, value="btn_vway")  # 첫번째 행.
        first_rows = btn_vway.find_elements(by=By.TAG_NAME, value="a")  # 첫번째 행 버튼들.

        photo = first_rows[0]  # 사진

        handle.button_click(photo)

        if not handle.close_alert(driver):
            driver.back()
            return

        main = driver.window_handles

        count = 0
        print(len(main))
        if len(main) < 3:
            driver.back()
            return

        driver.switch_to.window(main[2])
        driver.execute_script("""
        up_window = window.open;
        window.open = function openWindow(url, blank){
            up_window(url, "_blank").focus();
        }""")

        # 사진 갯수
        wait.element_locate(driver, By.CLASS_NAME, "conList")
        conList = driver.find_element(by=By.CLASS_NAME, value="conList")
        photo_list = conList.find_elements(by=By.TAG_NAME, value="li")
        length = len(photo_list)
        current = 1
        for elem in photo_list:
            count = count + 1
            handle.button_click(elem.find_element(by=By.TAG_NAME, value="a"))
            wait.element_click(driver, By.CSS_SELECTOR,
                               "#frm > div.popup_wrap > div.popup_container > div > div.pop_viewer > a > img")
            handle.button_click(driver.find_element(by=By.CSS_SELECTOR,
                                                    value="#frm > div > div.popup_container >\
                                                     div > div.pop_viewer > a > img"))

            sub = driver.window_handles
            driver.switch_to.window(sub[3])
            wait.element_locate(driver, By.TAG_NAME, "img")
            if count == 1:
                self.file['TYPE'] = 'MAIN_PHOTO'
            else:
                self.file['TYPE'] = 'SUB_PHOTO'

            photo_url = driver.find_element(by=By.TAG_NAME, value="img").get_attribute("src")
            self.file['LINK'] = photo_url
            self.get_data()

            driver.close()
            driver.switch_to.window(sub[2])
            if current > 3 and current != length:
                wait.element_click(driver, By.CLASS_NAME, "btn_down")
                handle.button_click(driver.find_element(by=By.CLASS_NAME, value="btn_down"))
            current = current + 1

        driver.close()
        driver.switch_to.window(main[0])
        driver.back()

    def load_registration_map(self, driver: webdriver.Chrome) -> None:
        """
        :desc 지적도 버튼 클릭 후 지적도 정보 저장.
        :param driver: 크롬 드라이버
        :return: None
        """
        wait.element_locate(driver, By.CLASS_NAME, "visual_inner")
        visual_inner = driver.find_element(by=By.CLASS_NAME, value="visual_inner")

        btn_vway = visual_inner.find_element(by=By.CLASS_NAME, value="btn_vway")  # 첫번째 행.
        first_rows = btn_vway.find_elements(by=By.TAG_NAME, value="a")  # 첫번째 행 버튼들.

        registration_map = first_rows[3]  # 지적도

        self.file['TYPE'] = 'REG_MAP'
        handle.button_click(registration_map)
        if not handle.close_alert(driver):
            driver.back()
            return
        main = driver.window_handles

        if len(main) < 3:
            driver.back()
            return

        driver.switch_to.window(main[2])

        wait.element_locate(driver, By.CLASS_NAME, "fwu.cm_txt_bu_01")
        elems = driver.find_elements(by=By.CLASS_NAME, value="fwu.cm_txt_bu_01")

        for elem in elems:
            self.file['LINK'] = elem.get_attribute("href")
            self.get_data()

        driver.close()
        driver.switch_to.window(main[0])
        driver.back()

    def load_location_map(self, driver: webdriver.Chrome) -> None:
        """
        :desc 위치도 클릭 후 데이터 적재
        :param driver: 크롬 드라이버
        :return: None
        """
        wait.element_locate(driver, By.CLASS_NAME, "visual_inner")
        visual_inner = driver.find_element(by=By.CLASS_NAME, value="visual_inner")

        btn_vway2 = visual_inner.find_element(by=By.CLASS_NAME, value="file_down_wrap")  # 두번째 행.
        second_rows = btn_vway2.find_elements(by=By.TAG_NAME, value="a")  # 두번째 행 버튼들.

        location_map = second_rows[0]  # 위치도

        self.file['TYPE'] = 'LOC_MAP'
        handle.button_click(location_map)

        if not handle.close_alert(driver):
            driver.back()
            return

        main = driver.window_handles

        if len(main) < 3:
            driver.back()
            return

        driver.switch_to.window(main[2])

        wait.element_locate(driver, By.CLASS_NAME, "fwu.cm_txt_bu_01")
        elems = driver.find_elements(by=By.CLASS_NAME, value="fwu.cm_txt_bu_01")

        for elem in elems:
            self.file['LINK'] = elem.get_attribute("href")
            self.get_data()

        driver.close()
        driver.switch_to.window(main[0])
        driver.back()

    def load_data(self, driver: webdriver.Chrome) -> None:
        """
        사진, 위치도, 지적도 버튼 적재하는 함수 호출
        :param driver: 크롬 드라이버
        :return: None
        """
        # 물건관리번호
        if wait.is_element_presence(driver, By.CLASS_NAME, "tab_wrap1.pos_rel"):
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
        else:
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")

        MNG_NO: str = tab_wrap.find_element(
            by=By.CSS_SELECTOR, value="div.finder03 >div > div.txt_top > p.fl.fwb > span:nth-child(2)").text
        self.file['MNG_NO'] = MNG_NO

        driver.execute_script("""
                up_window = window.open;
            window.open = function openWindow(url, blank){
                up_window(url, "_blank").focus();
            }""")

        self.load_photo(driver)
        self.load_registration_map(driver)
        self.load_location_map(driver)


def get_data(driver: webdriver.Chrome, announce_no: str) -> None:
    """
    :desc MULGUN_FILE 클래스로 사진, 지적도, 위치도 정보 적재.
    :param driver: 크롬 드라이버
    :param announce_no: 공고 번호
    :return: None
    """
    file = MULGUN_FILE(announce_no)

    file.load_data(driver)