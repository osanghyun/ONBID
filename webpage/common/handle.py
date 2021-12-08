from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
import selenium.common.exceptions
from selenium import webdriver


def close_popup(driver: webdriver.Chrome) -> None:
    """
    메인창을 제외한 창 닫기
    :param driver: 크롬 드라이버
    :return: None
    """
    main: list = driver.window_handles
    for handle in main:
        handle: str
        if handle != main[0]:
            driver.switch_to.window(handle)
            driver.close()
    driver.switch_to.window(main[0])


def close_alert(driver: webdriver.Chrome) -> bool:
    """
    버튼을 클릭시 데이터가 존재하지않으면 alert가 뜨는 경우를 다룸.
    :param driver: 크롬 드라이버
    :return: alert가 뜨면 False, 뜨지 않으면 True.
    """
    try:
        WebDriverWait(driver, 1, poll_frequency=0.01).until(EC.alert_is_present(), "팝업 대기")
        alert = driver.switch_to.alert
        alert.accept()
        main = driver.window_handles
        driver.switch_to.window(main[0])
        print("handle_alert 함수 호출 결과 : 데이터 비존재.")
        return False
    except selenium.common.exceptions.TimeoutException:
        print("handle_alert 함수 호출 결과 : 데이터 존재.")
        return True


def button_click(button: WebElement) -> None:
    """
    외부 입력에 의해 클릭에 문제가 발생함을 방지하기 위해서
    :param button: 클릭하고자 하는 WebElement
    :return: None
    """
    try:
        button.click()
    except selenium.common.exceptions.ElementClickInterceptedException:
        button.click()