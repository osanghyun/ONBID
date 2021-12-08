from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium import webdriver
from ONBID.webpage.common import handle
from ONBID.webpage.common import wait
import time


def insert_idpw(driver: webdriver.Chrome, id_param: str, pw_param: str) -> None:
    """
    id와 pw 입력.
    :param driver: 크롬 드라이버
    :param id_param: id
    :param pw_param: pw
    :return: None
    """
    wait.element_locate(driver, By.ID, "usrId")
    id_part: WebElement = driver.find_element(By.ID, "usrId")
    pw_part: WebElement = driver.find_element(By.ID, "encpw")

    if id_part == WebElement:
        id_part.click()
    else:
        id_part = driver.find_element(By.ID, "usrId")
        id_part.click()

    time.sleep(1)
    id_part.send_keys(id_param)
    time.sleep(0.1)
    id_part.clear()
    for word in id_param:
        id_part.send_keys(word)
        time.sleep(0.1)

    if pw_part == WebElement:
        pw_part.click()
    else:
        pw_part = driver.find_element(by=By.ID, value="encpw")
        pw_part.click()

    time.sleep(1)
    pw_part.clear()
    time.sleep(0.1)
    for word in pw_param:
        pw_part.send_keys(word)
        time.sleep(0.1)
    time.sleep(1)

    wait.element_click(driver, By.CSS_SELECTOR, "#frm > fieldset > a")
    submit_part = driver.find_element(by=By.CSS_SELECTOR, value="#frm > fieldset > a")
    submit_part.click()

    if not handle.close_alert(driver):
        insert_idpw(driver, id_param, pw_param)


def login(driver: webdriver.Chrome, id_param: str, pw_param: str) -> None:
    """
    로그인.
    :param driver: 크롬 드라이버
    :param id_param: 아이디
    :param pw_param: 패스워드
    :return: None
    """
    wait.element_click(driver, By.CSS_SELECTOR, "#Wrap > div.headerWrap > div.header > div.util > div > a:nth-child(1)")
    driver.find_element(By.CSS_SELECTOR,
                        "#Wrap > div.headerWrap > div.header > div.util > div > a:nth-child(1)").click()

    insert_idpw(driver, id_param, pw_param)

    main: list = driver.window_handles

    if len(main) == 2:
        driver.switch_to.window(main[1])

        if wait.is_element_presence(driver, By.CSS_SELECTOR, "#dplcLoginPop > div.popup_header > h2"):
            title: str = driver.find_element(by=By.CSS_SELECTOR,
                                             value="#dplcLoginPop > div.popup_header > h2").text
            if "중복 로그인 알림" in title:
                wait.element_click(driver, By.CLASS_NAME, "cm_btn_b_f.close_pop")
                driver.find_element(by=By.CLASS_NAME, value="cm_btn_b_f.close_pop").click()

                """
                time.sleep() 말고 다른 방법이 있는지 생각.
                """
                time.sleep(7)
                main = driver.window_handles
                if len(main) == 2:
                    driver.switch_to.window(main[1])

        driver.close()
        driver.switch_to.window(main[0])