import streamlit as st

st.set_page_config(page_title="울산대학교 미래 동행", layout="centered")

# CSS로 디자인 요소 강화 (울산대 브랜드 컬러 느낌)
st.markdown("""
    <style>
    .stButton>button {width: 100%; border-radius: 20px; background-color: #004a99; color: white;}
    </style>
    """, unsafe_allow_html=True)

st.title("울산대학교와 함께하는 미래")
st.write("울산대학교의 발전을 응원해 주셔서 감사합니다. 기부자님의 소중한 마음을 전달해 주세요.")

# 단계별 진행을 위한 세션 상태 관리
if 'step' not in st.session_state: st.session_state.step = 1

# Step 1: 기부처 및 금액 선택
if st.session_state.step == 1:
    st.header("Step 1. 마음 전달하기")
    fund_purpose = st.radio("어디를 응원하고 싶으신가요?", ["교육여건개선기금", "지정기금(학과/연구소/장학)"])
    
    if fund_purpose == "지정기금(학과/연구소/장학)":
        specific_dept = st.text_input("응원하실 부서나 학과를 입력해 주세요.")
        specific_use = st.radio("기부금 사용처", ["장학", "교육(위임)", "연구", "건축(시설)"], horizontal=True)
    
    amount = st.number_input("기부 희망 금액 (원)", min_value=10000, step=10000)
    
    if st.button("다음 단계로"):
        st.session_state.step = 2
        st.rerun()

# Step 2: 기부자 정보
elif st.session_state.step == 2:
    st.header("Step 2. 기부자 정보")
    name = st.text_input("성함 (법인명)")
    reg_num = st.text_input("주민(사업자) 등록번호 (영수증 발급용)")
    phone = st.text_input("휴대폰 번호")
    email = st.text_input("E-Mail (소식지 수신용)")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("이전"): st.session_state.step = 1; st.rerun()
    with col2:
        if st.button("다음 단계로"): st.session_state.step = 3; st.rerun()

# Step 3: 결제 및 완료
elif st.session_state.step == 3:
    st.header("Step 3. 소중한 약정")
    pay_method = st.radio("기부 결제 방식", ["1회 기부(일시불)", "정기 기부(CMS)", "교직원 급여공제"])
    
    privacy = st.checkbox("개인정보 수집 및 이용에 동의합니다. (필수)")
    
    if st.button("약정 완료하기"):
        if privacy:
            st.balloons()
            st.success("울산대학교의 미래에 함께해 주셔서 진심으로 감사합니다!")
        else:
            st.error("개인정보 동의가 필요합니다.")