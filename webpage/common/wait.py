from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
from selenium import webdriver
import sys


def element_click(driver: webdriver.Chrome, by_type: str, locator: str) -> None:
    """
    :desc 5초안에 WebElement가 클릭이 가능한 상태가 되면 정상동작 아닐시 프로그램 종료.
    :param driver: 크롬 드라이버
    :param by_type: By 유형
    :param locator: 위치
    :return: None
    """
    print(f"element_click_wait 함수 호출 ({by_type}, {locator})")
    try:
        WebDriverWait(driver, 5, poll_frequency=0.01).until(EC.element_to_be_clickable((by_type, locator)))
        return
    except selenium.common.exceptions.TimeoutException:
        print(str(by_type) + str(locator) + " Timeout Error")
        driver.close()
        sys.exit()


def element_locate(driver: webdriver.Chrome, by_type: str, locator: str) -> None:
    """
    :desc 5초안에 WebElement가 찾아지면 정상동작 아닐시 프로그램 종료.
    :param driver: 크롬 드라이버
    :param by_type: By 유형
    :param locator: 위치
    :return: None
    """
    print(f"element_click_wait 함수 호출 ({by_type}, {locator})")
    try:
        WebDriverWait(driver, 5, poll_frequency=0.01).until(EC.presence_of_element_located((by_type, locator)))
        return
    except selenium.common.exceptions.TimeoutException:
        print(str(by_type) + str(locator) + " Timeout Error")
        driver.close()
        sys.exit()


def is_element_presence(driver: webdriver.Chrome, by_type: str, locator: str) -> bool:
    """
    :desc 목표 WebElement가 존재하는지 검사
    :param driver:  크롬 드라이버
    :param by_type: By 유형
    :param locator: 위치
    :return: 목표 WebElement가 존재하면 True, 아니면 False
    """
    try:
        WebDriverWait(driver, 2, poll_frequency=0.01).until(EC.presence_of_element_located((by_type, locator)))
        print(f"is_element_presence 함수 호출 ({by_type}, {locator}) 결과 : 존재")
        return True
    except selenium.common.exceptions.TimeoutException:
        print(f"is_element_presence 함수 호출 ({by_type}, {locator}) 결과 : 비존재")
        return False