from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from ONBID.webpage.common import wait
from ONBID.webpage.common import handle
from selenium import webdriver


def click_gonggo(driver: webdriver.Chrome) -> None:
    """
    :desc 공고목록 페이지로 이동
    :param driver: 크롬 드라이버
    :return: None
    """
    wait.element_click(driver, By.CSS_SELECTOR, "#lnbWrap > div.lnb > ul > li:nth-child(3) > a")
    handle.button_click(driver.find_element(By.CSS_SELECTOR, "#lnbWrap > div.lnb > ul > li:nth-child(3) > a"))

    wait.element_click(driver, By.LINK_TEXT, "공고목록")
    handle.button_click(driver.find_element(By.LINK_TEXT, "공고목록"))


def set_gonggo_date(driver: webdriver.Chrome) -> None:
    """
    :desc 검색 조건의 공고 날짜 설정
    :param driver: 크롬 드라이버
    :return:
    """
    wait.element_click(driver, By.CSS_SELECTOR, "input#searchPbctBegnDtm")
    basic: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="input#searchPbctBegnDtm")
    basic.clear()

    wait.element_click(driver, By.CSS_SELECTOR, "input#searchPbctClsDtm")
    basic: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="input#searchPbctClsDtm")
    basic.clear()

    wait.element_click(driver, By.CSS_SELECTOR, "input#searchBegnPlnmDt")
    start_date: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="input#searchBegnPlnmDt")
    if start_date == WebElement:
        handle.button_click(start_date)
        start_date.clear()
        start_date.send_keys('2021-02-01')
    else:
        start_date: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="input#searchBegnPlnmDt")
        handle.button_click(start_date)
        start_date.clear()
        start_date.send_keys('2021-02-01')

    wait.element_click(driver, By.CSS_SELECTOR, "input#searchClsPlnmDt")
    end_date: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="input#searchClsPlnmDt")
    if end_date == WebElement:
        handle.button_click(end_date)
        end_date.clear()
        end_date.send_keys('2022-02-01')
    else:
        end_date: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="input#searchClsPlnmDt")
        handle.button_click(end_date)
        end_date.clear()
        end_date.send_keys('2022-02-01')


def search(driver: webdriver.Chrome) -> None:
    """
    :desc 공고 검색 버튼 클릭.
    :param driver: 크롬드라이버
    :return: None
    """
    wait.element_click(driver, By.CSS_SELECTOR,
                       "#Contents > div.tab_wrap2.pos_rel.mt20 > div.op_detail_show > div > a.cm_btn_w_o.ml3")
    driver.find_element(
        by=By.CSS_SELECTOR,
        value="#Contents > div.tab_wrap2.pos_rel.mt20 > div.op_detail_show > div > a.cm_btn_w_o.ml3").click()


def set_elem_hundred(driver: webdriver.Chrome) -> None:
    """
    :desc 테이블 elem 100개씩 보이도록 정렬
    :param driver:
    :return:
    """
    # 100줄씩 설정.
    wait.element_click(driver, By.CSS_SELECTOR, "#pageUnit > option:nth-child(4)")
    handle.button_click(driver.find_element(by=By.CSS_SELECTOR, value="#pageUnit > option:nth-child(4)"))

    # 정렬.
    wait.element_click(driver, By.CLASS_NAME, "cm_btn_tnt")
    handle.button_click(driver.find_element(by=By.CLASS_NAME, value="cm_btn_tnt"))


def is_table_end(driver: webdriver.Chrome, elem_index: int) -> bool:
    """
    :desc 스캔되지 않은 테이블 element 존재하는지 검사.
    :param driver: 크롬 드라이버
    :param elem_index: 테이블의 몇번째 데이터인지
    :return: 마지막이면 True, 아니면 False 반환
    """
    # 테이블 선택.
    wait.element_locate(driver, By.CLASS_NAME, "op_tbl_type1")
    table = driver.find_element(by=By.CLASS_NAME, value="op_tbl_type1")

    # 테이블 바디 선택.
    body = table.find_element(by=By.TAG_NAME, value="tbody")

    # 테이블 행 선택.
    trs = body.find_elements(by=By.TAG_NAME, value="tr")

    if elem_index >= len(trs):
        return True

    if "없습니다" in trs[0].text:
        return True

    return False


def is_cancel_gonggo(driver: webdriver.Chrome, elem_index: int) -> bool:
    """
    :desc 취소 공고인지 검사
    :param driver: 크롬 드라이버
    :param elem_index: 테이블의 몇번째 데이터인지
    :return: 취소공고면 True, 아니면 False
    """

    wait.element_locate(driver, By.CSS_SELECTOR,
                        f'#Contents > table > tbody > tr:nth-child({elem_index+1})\
                         > td.al.pos_rel > dl > dd.badge_wrap.mt5')

    badge = driver.find_element(By.CSS_SELECTOR, "#Contents > table > tbody > tr:nth-child(" +
                                f'{elem_index+1}' + ") > td.al.pos_rel > dl > dd.badge_wrap.mt5")

    str_data: str = badge.find_element(By.TAG_NAME, value="em").text

    if "취소공고" in str_data:
        return True

    return False


def gonggo_detail_click(driver: webdriver.Chrome, gonggo_index: int) -> None:
    """
    :desc 공고 번호 클릭을 통해 공고 상세로 이동.
    :param driver: 크롬 드라이버
    :param gonggo_index: 테이블의 몇번째 데이터인지
    :return: None
    """
    table = driver.find_element(by=By.CLASS_NAME, value="op_tbl_type1")

    body = table.find_element(by=By.TAG_NAME, value="tbody")

    trs = body.find_elements(by=By.TAG_NAME, value="tr")

    tds = trs[gonggo_index].find_elements(by=By.TAG_NAME, value="td")

    handle.button_click(tds[0].find_element(by=By.CSS_SELECTOR, value="dl > dt > label > a"))


def set_open_new_window_to_tap(driver: webdriver.Chrome) -> None:
    """
    :desc 새로운 윈도우 창을 탭 형태로 생성되게 만듬.
    :param driver: 크롬 드라이버
    :return: None
    """
    driver.execute_script("""
    
    up_window = window.open;
    window.open = function openWindow(url, blank){
        up_window(url, "_blank").focus();
    }
    
    close_window = window.close;
    window.close = function closeWindow(){
        window.location.reload();
    }
    
""")


def open_gonggo_mulgun_table_tab(driver: webdriver.Chrome) -> None:
    """
    :desc 공고 상세의 물건 목록 버튼 클릭.
    :param driver: 크롬 드라이버
    :return: None
    """
    driver.execute_script("""
        up_window = window.open;
    window.open = function openWindow(url, blank){
        up_window(url, "_blank").focus();
    }""")

    wait.element_click(driver, By.CSS_SELECTOR,
                       "#Contents > div.top_wrap2.pos_rel > div.top_detail_btns > p > a:nth-child(1)")
    driver.find_element(By.CSS_SELECTOR,
                        "#Contents > div.top_wrap2.pos_rel > div.top_detail_btns > p > a:nth-child(1)").click()

    main = driver.window_handles
    assert len(main) == 2

    driver.switch_to.window(main[1])
    assert "온비드" in driver.title


def close_gonggo_mulgun_table_tab(driver: webdriver.Chrome) -> None:
    """
    :desc 물건 목록 탭 닫기.
    :param driver: 크롬 드라이버
    :return: None
    """
    handle.close_popup(driver)
    assert "공고목록" in driver.title


def open_mulgun_detail_tab(driver: webdriver.Chrome, mulgun_index: int) -> None:
    """
    :desc 물건 목록의 물건 관리 번호를 클릭하여 물건 상세 페이지로 이동
    :param driver: 크롬 드라이버
    :param mulgun_index: 테이블의 몇번째 데이터인지
    :return: None
    """
    main = driver.window_handles
    assert len(main) == 2

    driver.switch_to.window(main[1])
    assert "온비드" in driver.title
    set_open_new_window_to_tap(driver)

    table = driver.find_element(by=By.CLASS_NAME, value="op_tbl_type1")

    body = table.find_element(by=By.TAG_NAME, value="tbody")

    trs = body.find_elements(by=By.TAG_NAME, value="tr")

    tds = trs[mulgun_index].find_elements(by=By.TAG_NAME, value="td")

    target: WebElement = tds[0].find_element(by=By.CSS_SELECTOR, value="div > dl > dt > a")

    handle.button_click(target)

    main = driver.window_handles
    assert len(main) == 2

    driver.switch_to.window(main[0])
    assert "물건검색" in driver.title


def move_to_mulgun_table(driver: webdriver.Chrome) -> None:
    """
    :desc 물건 목록 테이블로 이동
    :param driver: 크롬 드라이버
    :return: None
    """
    main = driver.window_handles
    assert len(main) == 2
    driver.switch_to.window(main[1])
    assert "온비드" in driver.title


def is_mulgun_budongsan(driver: webdriver.Chrome, mulgun_index: int) -> bool:
    """
    :desc 물건 목록의 물건이 부동산에 속한 물건인지 판별
    :param driver: 크롬 드라이버
    :param mulgun_index: 테이블의 몇번째 데이터인지
    :return: 부동산에 속하면 True, 아니면 False
    """
    Category: WebElement = driver.find_element(By.CSS_SELECTOR,
                                               "#frm > div > div.popup_container > table > tbody > tr:nth-child" +
                                               f'({mulgun_index+1})' + " > td.al.pos_rel > div > dl > dd.tpoint_03")

    str_data = Category.text

    if "토지" in str_data:
        return True
    elif "주거용건물" in str_data:
        return True
    elif "상가용및업무용건물" in str_data:
        return True
    elif "산업용및기타특수용건물" in str_data:
        return True
    elif "용도복합용건물" in str_data:
        return True
    else:
        return False


def click_pre_ipchal(driver: webdriver.Chrome) -> None:
    """
    :desc 물건 상세의 입찰 이력 버튼 클릭
    :param driver: 크롬 드라이버
    :return: None
    """
    if wait.is_element_presence(driver, By.CLASS_NAME, "tab_wrap1.pos_rel"):
        ipchal_button: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                        value="#Contents > div.tab_wrap1.pos_rel > \
                                                        ul > li:nth-child(2) > a")
    else:
        ipchal_button: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                        value="#Contents > div.tab_wrap.pos_rel > \
                                                        ul > li:nth-child(2) > a")

    handle.button_click(ipchal_button)
