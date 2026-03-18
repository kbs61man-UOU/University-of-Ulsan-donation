import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="울산대학교 발전기금 약정서", layout="centered")

st.title("울산대학교 발전기금 약정서")
st.write("위의 내용과 같이 울산대학교 발전기금모금에 참여하고자 합니다.")

st.header("1. 기부자 정보")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("성명 (법인명) *")
with col2:
    reg_num = st.text_input("주민(사업자) 등록번호 *", placeholder="예: 800101-1234567")

donor_type = st.radio(
    "기부자 구분 *", 
    ["동문", "학생", "학부모", "교직원", "기업", "일반", "후원의집", "기타"],
    horizontal=True
)

col3, col4 = st.columns(2)
with col3:
    phone = st.text_input("휴대폰 번호 *")
with col4:
    email = st.text_input("E-Mail")
    
st.write("직장 정보 (선택)")
col5, col6, col7 = st.columns(3)
with col5:
    company = st.text_input("직장명")
with col6:
    department = st.text_input("부서")
with col7:
    position = st.text_input("직위")

st.divider()

st.header("2. 약정 내역")
amount = st.number_input("약정액 (원) *", min_value=0, step=10000)

fund_purpose = st.radio("기금 용도 *", ["교육여건개선기금", "지정기금"])

# 폼(form)을 해제했으므로 이제 지정기금 클릭 시 즉시 아래 항목이 나타납니다.
if fund_purpose == "지정기금":
    st.caption("특정 부서에 지정기탁하시는 경우, 기탁금 중 10%가 교육여건개선기금으로 편입됩니다. (장학금 제외)")
    
    specific_dept = st.text_input("지정 부서 (예: 융합대학, 특정학과, 연구소 등)")
    
    specific_use = st.radio(
        "지정 용도 *", 
        ["교육(위임)", "연구", "장학", "건축(시설)"],
        horizontal=True
    )

st.divider()

st.header("3. 납부 방법")
payment_method = st.radio(
    "납부 방법 선택 *", 
    ["일시불", "자동이체 (CMS)", "급여공제"],
    horizontal=True
)

# 납부 방법 선택에 따라 화면이 실시간으로 바뀝니다.
if payment_method == "일시불":
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        pay_date = st.date_input("기부 예정일")
    with p_col2:
        bank_choice = st.selectbox("거래은행", ["경남은행", "국민은행", "농협", "기타"])
        
elif payment_method == "자동이체 (CMS)":
    st.info("CMS는 울산대학교가 금융결제원에 자동이체 출금을 의뢰하는 방법입니다. 송금 수수료가 없습니다.")
    cms_col1, cms_col2, cms_col3 = st.columns(3)
    with cms_col1:
        cms_bank = st.selectbox("거래은행", ["경남은행", "국민은행", "농협", "하나은행", "신한은행", "기타"])
    with cms_col2:
        cms_owner = st.text_input("예금주")
    with cms_col3:
        cms_account = st.text_input("계좌번호")
        
    cms_col4, cms_col5 = st.columns(2)
    with cms_col4:
        cms_monthly_amount = st.number_input("매월 약정금액 (원)", min_value=0, step=10000)
    with cms_col5:
        cms_transfer_date = st.radio("이체일", ["15일", "25일"], horizontal=True)
        
    cms_period = st.text_input("기부기간 (예: 2026년 4월 ~ 2027년 3월, 총 12회)")

elif payment_method == "급여공제":
    st.info("울산대학교 교직원만 해당됩니다.")
    sal_col1, sal_col2 = st.columns(2)
    with sal_col1:
        sal_monthly_amount = st.number_input("매월 약정금액 (만원)", min_value=0, step=1)
    with sal_col2:
        st.text_input("공제일", value="매월 15일", disabled=True)
        
    sal_period = st.text_input("기부기간 (예: 2026년 4월 부터, 총 12회)")

st.divider()

st.header("4. 개인정보 수집 및 이용 동의")
st.write("개인정보 이용목적: 기부금영수증 발급, 후원자 예우 프로그램 제공 등")
privacy_consent = st.checkbox("개인정보 수집 및 이용에 동의합니다. (필수)")

st.divider()

st.header("5. 기부정보 공개 여부")
st.write("※ 기부사실 공개를 원하지 않는 곳에 체크해 주세요.")

chk_col1, chk_col2, chk_col3, chk_col4 = st.columns(4)
with chk_col1: hide_list = st.checkbox("명단(홈페이지/책자)")
with chk_col2: hide_article = st.checkbox("교내기사")
with chk_col3: hide_press = st.checkbox("언론보도")
with chk_col4: hide_internal = st.checkbox("대학 내부회의")

# 제출 버튼 (st.form_submit_button -> st.button으로 변경)
if st.button("약정서 접수하기", use_container_width=True):
    if not name or not phone or not reg_num or amount == 0:
        st.error("성명, 주민등록번호, 휴대폰 번호 및 약정액 등 필수 항목을 모두 입력해 주세요.")
    elif fund_purpose == "지정기금" and 'specific_use' not in locals():
         st.error("지정기금의 용도를 선택해 주세요.")
    elif not privacy_consent:
        st.error("개인정보 수집 및 이용에 동의해야 접수가 가능합니다.")
    else:
        st.success(f"감사합니다! {name}님의 약정서가 성공적으로 접수되었습니다.")