from selenium.webdriver.common.by import By
from ONBID.webpage.common import wait
from selenium import webdriver


def is_table_end(driver: webdriver.Chrome, mulgun_index: int) -> bool:
    """
    물건 목록에 스캔되지 않은 물건이 존재하는지 검사.
    :param driver: 크롬 드라이버
    :param mulgun_index: 물건 테이블에서 현재 테이블의 순번
    :return: table 끝이면 True, 아니면 False
    """
    # 테이블 선택.
    wait.element_locate(driver, By.CLASS_NAME, "op_tbl_type1")
    table = driver.find_element(by=By.CLASS_NAME, value="op_tbl_type1")

    # 테이블 바디 선택.
    body = table.find_element(by=By.TAG_NAME, value="tbody")

    # 테이블 행 선택.
    trs = body.find_elements(by=By.TAG_NAME, value="tr")

    if mulgun_index >= len(trs):
        return True

    if "없습니다" in trs[0].text:
        return True

    return False