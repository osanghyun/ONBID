## 온비드_부동산 크롤링
    Main : ONBID_GONGGO.py

    명령어 : python3 ONBID_GONGGO.py

### 동작 순서

    1. ONBID 메인 홈페이지 접속

    2. 로그인

    3. 부동산 -> 공고 -> 공고 목록

    4. 공고일자 설정 -> 검색

    5. 100줄씩 보기 정렬

    6. 공고 목록 테이블 Loop (테이블에 존재하는 공고 하나씩 방문, 취소 공고 제외)

        6.1 공고 정보 저장 ( basic_info.py )
        
        6.2 공고 상세로 이동

        6.3 공고 상세 정보 저장 ( gonggo_detail_info.py )

        6.4 공고물건 보기 클릭

        6.5 100줄씩 보기 정렬

        6.6 공고 물건 목록 테이블 Loop (테이블에 존재하는 물건 하나씩 방문, 부동산 카테고리가 아닌 물건 제외)

            6.6.1 물건 상세로 이동

            6.6.2 물건 세부 정보 저장 ( mulgun_detail.py )

            6.6.3 물건 면적 정보 저장 ( mulgun_area.py )

            6.6.4 물건 위치 및 부근현황, 명도이전책임 저장 ( mulgun_locate_myungdo.py )

            6.6.5 물건 감정평가 정보 저장 ( mulgun_gamjung.py )

            6.6.6 물건 권리분석 기초 정보 저장 ( mulgun_baebun.py )

            6.6.7 물건 임대차 정보 저장 ( mulgun_imdae.py )

            6.6.8 물건 사진, 지적도, 위치도 저장 ( mulgun_file.py )

            6.6.9 물건 회차별 입찰 정보 저장 ( mulgun_ipchal.py )

            6.6.10 입찰 이력 클릭

            6.6.11 입찰 이력 정보 저장 ( mulgun_ipchal_history.py )

        

### ONBID.webpage.common [패키지]

#### setup.py [모듈]
    
    def get_driver() -> Chrome: 크롬 드라이버의 경로와 다운로드 경로 설정.
    
    def main_page(Chrome) -> None: 온비드 메인 홈페이지 접속.

    def next_page(Chrome) -> bool: 다음 페이지로 이동. 끝에 도달하면 True, 아니면 False.

#### login.py [모듈]

    def insert_idpw(Chrome, str, str) -> None: id와 pw 입력.

    def login(Chrome, str, str) -> None: 로그인.

#### handle.py [모듈]

    def close_popup(Chrome) -> None: 메인창을 제외한 창 닫기.
    
    def close_alert(Chrome) -> bool: 버튼을 클릭시 데이터가 존재하지않으면 alert가 뜨는 경우를 다룸.

    def button_click(WebElement) -> None: 외부 입력에 의해 클릭에 문제가 발생함을 방지하기 위해서

#### wait.py [모듈]

    def element_click(Chrome, str, str) -> None: 5초안에 WebElement가 클릭이 가능한 상태가 되면 정상동작 아닐시 프로그램 종료.

    def element_locate(Chrome, str, str) -> None: 5초안에 WebElement가 찾아지면 정상동작 아닐시 프로그램 종료.

    def is_element_presence(Chrome, str, str) -> bool: 목표 WebElement가 존재하는지 검사.

### ONBID.webpage.gonggo [패키지]

#### setup.py [모듈]

    def click_gonggo(Chrome) -> None: 공고 목록 페이지로 이동.

    def set_gonggo_date(Chrome) -> None: 검색 조건의 공고 날짜 설정.

    def serach(Chrome) -> None: 공고 검색 버튼 클릭.

    def set_elem_hundred(Chrome) -> None: 테이블 데이터 100개씩 보이도록 조정.

    def is_table_end(Chrome, int) -> bool: 테이블 데이터를 다 읽었는지 검사.

    def is_cancel_gonggo(Chrome, int) -> bool: 취소 공고인지 검사.

    def gonggo_detail_click(Chrome, int) -> None: 공고 번호 클릭을 통해 공고 상세로 이동.

    def set_open_new_window_to_tap(Chrome) -> None: 새로운 윈도우 창을 탭 형태로 생성되게 만듬.

    def open_gonggo_mulgun_table_tab(Chrome) -> None: 공고 상세의 물건 목록 버튼 클릭.

    def close_gonggo_mulgun_table_tab(Chrome) -> None: 물건 목록 탭 닫기.

    def open_mulgun_detail_tab(Chrome, int) -> None: 물건 목록의 물건 관리 번호를 클릭하여 물건 상세 페이지로 이동.

    def move_to_mulgun_table(Chrome) -> None: 물건 목록 테이블로 이동.

    def is_mulgun_budongsan(Chrome, int) -> bool: 물건 목록의 물건이 부동산에 속한 물건인지 판별.

    def click_pre_ipchal(Chrome) -> None: 물건 상세의 입찰 이력 버튼 클릭.

#### basic_info.py [모듈]
    
    class GONGGO_BASIC: 공고 요약 정보를 적재.
    
    def get_data(Chrome, int) -> dict: 공고 목록 테이블에서 요약 정보 적재 후 반환.

#### gonggo_detail_info.py [모듈]

    class GONGGO_DETAIL: 공고 상세 정보 적재.

    def get_data(Chrome, dict) -> None: 공고 상세 정보와 공고문 전문, 공고 첨부파일, 공고물건 입찰정보 적재.
    
#### mulgun_area.py [모듈]

    class MULGUN_AREA: 물건 면적 정보를 적재.

    def get_data(Chrome, str) -> None: 물건 세부 정보 탭을 클릭 후 면적 정보 적재.

#### mulgun_baebun.py [모듈]

    class MULGUN_BAEBUN: 권리 분석 기초 정보의 배분요구 및 채권신고현황 정보 적재 (압류재산)

    def get_data(Chrome, str) -> None: 물건관리번호를 저장하고 압류재산 정보 탭 클릭 후 권리분석 기초정보 존재 여부 체크

#### mulgun_detail.py [모듈]

    class MULGUN_DETAIL: 물건 상세 데이터 저장.
    
    def get_data(Chrome, str) -> None: MULGUN_DETAIL 클래스 인스턴스에 물건 상세 데이터 저장.

#### mulgun_file.py [모듈]

    class MULGUN_FILE: 물건 사진, 지적도, 위치도 정보 적재.

    def get_data(Chrome, str) -> None: MULGUN_FILE 클래스로 사진, 지적도, 위치도 정보 적재.

#### mulgun_gamjung.py [모듈]

    class MULGUN_GAMJUNG: 물건 감정평가 정보 적재.

    def get_data(Chrome, str) -> None: 물건 세부 정보 버튼이 존재하면 감정평가 정보 적재하는 MULGUN_GAMJUNG 클래스 생성 후 호출

#### mulgun_imdae.py [모듈]

    class MULGUN_IMDAE: 압류재산 정보 탭의 임대차 정보 적재.

    def get_data(.Chrome, str) -> None: 압류재산 정보 탭이 존재하면 임대차 정보를 적재하는 MULGUN_IMDAE 클래스에 데이터 적재.

#### mulgun_ipchal.py [모듈]

    class IPCHAL: 회차별 입찰 정보 적재.

    def get_data(Chrome, str) -> None: :desc 입찰 정보 탭이 존재하면 IPCHAL 클래스를 호출하여 회차별 입찰정보 적재.

#### mulgun_ipchal_history.py [모듈]

    class IPCHAL_HISTORY: 입찰 이력 정보 적재.

    def get_data(Chrome, str) -> None: 물건 관리 번호 적재 후 입찰 이력 기본 정보와 상세 정보를 적재하는 IPCHAL_HISTORY 클래스 호출

#### mulgun_locate_myungdo.py [모듈]

    class MULGUN_LOCATE_MYUNGDO: 물건 세부정보 탭의 위치 및 이용현황 데이터 적재

    def get_data(Chrome, str) -> None: 물건 세부 정보 탭이 존재하면 MULGUN_LOCATE_MYUNGDO 클래스를 호출하여 위치 및 이용현황 데이터 적재

### ONBID.webpage.mulgun [패키지]
#### setup.py [모듈]

    def is_table_end(Chrome, int) -> bool: 물건 목록 테이블에 스캔되지 않은 물건이 존재하는지 검사