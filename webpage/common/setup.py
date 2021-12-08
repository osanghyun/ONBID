from selenium.webdriver.common.by import By
from ONBID.webpage.common import handle
from ONBID.webpage.common import wait
from selenium import webdriver
import re


def get_driver() -> webdriver.Chrome:
    """
    :desc 다운로드 경로와 크롬 드라이버 경로 설정.
    :return: webdriver.Chrome
    """
    options: webdriver.ChromeOptions = webdriver.ChromeOptions()

    options.add_experimental_option("prefs", {
        "download.default_directory": '/Users/osanghyun/PycharmProjects/DBProject2/ONBID/FileDirectory',
        "safebrowsing.enabled": True
    })

    chrome_driver_path: str = '/Users/osanghyun/PycharmProjects/DBProject2/ONBID/chromedriver'

    driver: webdriver.Chrome = webdriver.Chrome(chrome_driver_path, options=options)

    return driver


def main_page(driver: webdriver.Chrome) -> None:
    """
    :desc 온비드 메인 홈페이지 접속.
    :param driver: 크롬드라이버
    :return: None
    """
    driver.get('https://www.onbid.co.kr/op/dsa/main/main.do')
    assert "온비드" in driver.title
    handle.close_popup(driver)


def click_budongsan(driver: webdriver.Chrome) -> None:
    """
    :desc 부동산 HOME 클릭.
    :param driver: 크롬드라이버
    :return: None
    """
    wait.element_click(driver, By.LINK_TEXT, "부동산")
    driver.find_element(by=By.LINK_TEXT, value="부동산").click()
    wait.element_locate(driver, By.CLASS_NAME, "op_box_form02_in")


def next_page(driver: webdriver.Chrome) -> bool:
    """
    :desc 다음 페이지로 이동.
    :param driver: 크롬 드라이버
    :return: 끝에 도달하면 True, 아니면 False
    """
    if not wait.is_element_presence(driver, By.CLASS_NAME, "active"):  # 현재 페이지번호 element가 존재하는지 검사.
        return True

    # page column 선택.
    paging = driver.find_element(by=By.CLASS_NAME, value="cm_paging.cl")

    # 최대 페이지 번호 계산.
    total_page_text = paging.find_element(by=By.TAG_NAME, value="p").text
    total_number = int(re.sub(r'[^\d]+', "", total_page_text))
    total_number = str(int(total_number / 100) + 1)

    # 페이지 길이, 현재 페이지 번호 계산.
    pages = paging.find_elements(by=By.TAG_NAME, value="a")
    page_count = len(pages)
    pre_page = paging.find_element(by=By.CLASS_NAME, value="active").text

    # 현재 페이지 번호가 최대 페이지 번호가 되면 True 반환.
    if total_number == pre_page:
        return True

    # 다음 페이지로 이동.
    for i in range(page_count):
        if pages[i].text == pre_page:
            pages[i + 1].click()
            return False