"""
울산대학교 발전기금 온라인 약정서
-------------------------------------------------
- 외부 업체 PDF 시안의 '한 페이지' 구조는 유지하되,
  단계(step)로 분산시키지 않고 번호가 매겨진 섹션으로 자연스럽게 흐르게 구성.
- 잘못된 용어(학살방법→납부방법, 유권자기금→지정기금 등) 교정.
- 기부자에게 불필요한 내부 행정용 필드는 제거하고, 선택 항목은 접어서 부담을 낮춤.

실행: streamlit run ulsan_donation_app.py   (Streamlit 1.14 이상 권장)
"""

import datetime
import streamlit as st

# ──────────────────────────────────────────────
# 기본 설정 / 브랜드 색상
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="울산대학교 발전기금 약정",
    page_icon="🎓",
    layout="centered",
)

# 학교 공식 브랜드 컬러가 확정되면 이 두 값만 바꾸면 전체 톤이 바뀝니다.
PRIMARY = "#00529b"        # 대표색 (네이비 블루)
PRIMARY_DARK = "#003e76"

st.markdown(
    f"""
    <style>
        .block-container {{ padding-top: 2.0rem; max-width: 760px; }}

        /* 섹션 제목 */
        .sec-title {{
            font-size: 1.15rem; font-weight: 700; color: {PRIMARY};
            margin: 1.8rem 0 0.2rem 0; padding-bottom: 0.4rem;
            border-bottom: 2px solid {PRIMARY};
        }}
        .sec-help {{ color: #667085; font-size: 0.88rem; margin: 0.2rem 0 0.6rem 0; }}

        /* 주요 버튼 */
        div.stButton > button {{
            width: 100%; height: 3rem; border: none; border-radius: 10px;
            background-color: {PRIMARY}; color: #fff; font-weight: 700;
        }}
        div.stButton > button:hover {{ background-color: {PRIMARY_DARK}; color: #fff; }}

        /* 안내 카드 */
        .info-card {{
            background: #f4f8fc; border: 1px solid #d8e6f3; border-radius: 10px;
            padding: 0.9rem 1.1rem; font-size: 0.88rem; color: #33475b; line-height: 1.65;
        }}
        .amount-chip {{
            display:inline-block; margin-top:0.4rem; padding:0.3rem 0.8rem;
            background:{PRIMARY}; color:#fff; border-radius:20px; font-weight:700;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


def section(title: str, help_text: str | None = None) -> None:
    st.markdown(f'<div class="sec-title">{title}</div>', unsafe_allow_html=True)
    if help_text:
        st.markdown(f'<div class="sec-help">{help_text}</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 머리말
# ──────────────────────────────────────────────
st.title("울산대학교 발전기금 약정")
st.write(
    "여러분의 따뜻한 마음이 울산대학교의 내일을 만듭니다. "
    "아래 내용을 작성해 주시면 약정이 접수됩니다."
)

donation_type = st.radio(
    "기부 유형",
    ["발전기금", "후원의 집"],
    horizontal=True,
    label_visibility="collapsed",
)

# ──────────────────────────────────────────────
# 1. 약정 내역  (의미를 먼저 — '어디에 쓰이는가'부터)
# ──────────────────────────────────────────────
section("1. 어디에 마음을 전하시겠어요?", "기부금이 어떤 목적에 쓰일지 선택해 주세요.")

fund_purpose = st.radio(
    "기금 용도",
    ["교육여건개선기금", "지정기금"],
    captions=[
        "대학 전반의 교육환경 개선에 두루 사용됩니다.",
        "특정 학과·연구소·장학 등 원하시는 곳에 사용됩니다.",
    ],
)

target_dept = ""
target_use = ""
if fund_purpose == "지정기금":
    target_dept = st.text_input(
        "지정 대상 (학과·연구소·기관명 등)",
        placeholder="예) 의과대학 / OO연구소 / OO장학금",
    )
    target_use = st.radio(
        "사용 목적", ["장학", "교육", "연구", "시설(건축)"], horizontal=True
    )

amount = st.number_input(
    "약정 금액 (원)",
    min_value=10_000, step=10_000, value=100_000,
    help="최소 1만 원부터 약정하실 수 있습니다.",
)
st.markdown(f'<span class="amount-chip">약정 금액 {amount:,.0f} 원</span>', unsafe_allow_html=True)

with st.expander("ℹ️ 기금 용도가 궁금하신가요?"):
    st.markdown(
        """
- **교육여건개선기금** : 대학의 교육환경 개선을 위한 일반기금입니다.
- **지정기금** : 특정 학과·연구소·장학 등 기부자께서 지정하신 목적에만 사용됩니다.

> 특정인을 지정한 기부는 「상속세 및 증여세법」상 상속·증여재산으로
> 해석될 수 있어 접수가 제한될 수 있습니다. 자세한 내용은 담당 부서로 문의해 주세요.
"""
    )

# ──────────────────────────────────────────────
# 2. 납부 방법   (※ PDF의 '학살방법' → '납부 방법' 으로 교정)
# ──────────────────────────────────────────────
section("2. 어떻게 납부하시겠어요?")

pay_method = st.radio(
    "납부 방법",
    ["일시 납부", "정기 납부 (CMS 자동이체)", "교직원 급여공제"],
)

pay_date = st.date_input("기부(출금) 예정일", value=datetime.date.today())

bank = ""
if pay_method == "정기 납부 (CMS 자동이체)":
    bank = st.selectbox(
        "거래 은행 (예금주: 울산대학교)",
        ["선택하세요", "국민", "신한", "우리", "하나", "농협", "기업", "경남", "부산", "기타"],
    )
elif pay_method == "교직원 급여공제":
    st.caption("급여에서 매월 공제됩니다. 공제 시작 월은 담당 부서에서 안내드립니다.")

# ──────────────────────────────────────────────
# 3. 기부자 정보  (꼭 필요한 항목만, 나머지는 접어 둠)
# ──────────────────────────────────────────────
section("3. 기부자 정보", "영수증 발급과 소식 전달에 필요한 최소한의 정보만 받습니다.")

name = st.text_input("이름 (법인명) *", placeholder="홍길동")
phone = st.text_input("휴대폰 *", placeholder="010-0000-0000")
email = st.text_input("이메일", placeholder="뉴스레터·기부금영수증 안내를 받으실 주소")

need_receipt = st.checkbox("기부금영수증(연말정산용) 발급을 원합니다.")
reg_num = ""
if need_receipt:
    reg_num = st.text_input(
        "주민(사업자)등록번호",
        help="기부금영수증 발급 용도로만 사용되며 안전하게 보관됩니다.",
    )

with st.expander("주소·직장 정보 입력 (선택)"):
    c1, c2 = st.columns([1, 2])
    with c1:
        zipcode = st.text_input("우편번호")          # PDF의 '인사번호' → '우편번호'
    with c2:
        addr1 = st.text_input("주소")
    addr2 = st.text_input("상세주소")
    company = st.text_input("직장명")
    c3, c4 = st.columns(2)
    with c3:
        work_dept = st.text_input("부서")            # PDF의 '부문/부분' → '부서'
    with c4:
        position = st.text_input("직위")

# ──────────────────────────────────────────────
# 4. 기부 사실 공개  (긍정적 프레이밍, 전부 선택)
# ──────────────────────────────────────────────
section(
    "4. 기부 사실을 알려도 될까요?",
    "기부자님의 선한 영향력을 함께 나누고 싶습니다. 허용하실 범위를 골라 주세요. (선택)",
)
disclose = st.multiselect(
    "공개 허용 범위",
    ["대학 홈페이지·기부 책자", "교내 기사(홈페이지·소식지)", "언론 보도", "대학 내부 회의 자료"],
    label_visibility="collapsed",
)

# ──────────────────────────────────────────────
# 5. 개인정보 수집·이용 동의 (필수)
# ──────────────────────────────────────────────
section("5. 개인정보 수집·이용 동의 *")
st.markdown(
    """
    <div class="info-card">
    <b>· 이용 목적</b> : 기부금영수증 발급, 후원 예우 서비스(뉴스레터·행사 초청 등) 제공, 출금(CMS) 처리<br>
    <b>· 수집 항목</b><br>
    &nbsp;&nbsp;– (필수) 이름(법인명), 휴대폰, 약정·납부 정보<br>
    &nbsp;&nbsp;– (선택) 주민(사업자)등록번호, 이메일, 주소, 직장 정보<br>
    <b>· 보유 기간</b> : 관계 법령에서 정한 보존 기간까지<br>
    울산대학교 대외협력팀은 「개인정보 보호법」 제15조 및 제24조의2에 따라
    개인정보를 수집·이용·처리합니다.
    </div>
    """,
    unsafe_allow_html=True,
)
agree = st.checkbox("위 내용을 확인했으며, 개인정보 수집·이용에 동의합니다. (필수)")

# ──────────────────────────────────────────────
# 제출
# ──────────────────────────────────────────────
st.markdown("---")
col_cancel, col_submit = st.columns([1, 2])
with col_cancel:
    cancelled = st.button("취소")
with col_submit:
    submitted = st.button("약정 신청하기")

if cancelled:
    st.info("작성을 취소했습니다. 언제든 다시 함께해 주세요.")

if submitted:
    errors = []
    if not name.strip():
        errors.append("이름(법인명)을 입력해 주세요.")
    if not phone.strip():
        errors.append("휴대폰 번호를 입력해 주세요.")
    if fund_purpose == "지정기금" and not target_dept.strip():
        errors.append("지정 대상(학과·연구소 등)을 입력해 주세요.")
    if need_receipt and not reg_num.strip():
        errors.append("영수증 발급을 위해 주민(사업자)등록번호를 입력해 주세요.")
    if pay_method == "정기 납부 (CMS 자동이체)" and bank in ("", "선택하세요"):
        errors.append("CMS 출금을 위해 거래 은행을 선택해 주세요.")
    if not agree:
        errors.append("개인정보 수집·이용에 동의해 주세요.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.balloons()
        st.success("약정이 정상 접수되었습니다. 울산대학교의 미래에 함께해 주셔서 진심으로 감사합니다. 🎓")

        purpose_text = fund_purpose
        if fund_purpose == "지정기금":
            purpose_text = f"지정기금 · {target_dept} ({target_use})"

        with st.container(border=True):
            st.markdown("#### 약정 요약")
            st.write(f"- **기부 유형** : {donation_type}")
            st.write(f"- **기금 용도** : {purpose_text}")
            st.write(f"- **약정 금액** : {amount:,.0f} 원")
            st.write(f"- **납부 방법** : {pay_method}")
            st.write(f"- **기부 예정일** : {pay_date:%Y-%m-%d}")
            if bank not in ("", "선택하세요"):
                st.write(f"- **거래 은행** : {bank}")
            st.write(f"- **기부자** : {name}")
            if disclose:
                st.write(f"- **공개 허용** : {', '.join(disclose)}")

# ──────────────────────────────────────────────
# 담당 정보
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style="font-size:0.85rem; color:#667085; line-height:1.7;">
    <b>문의</b> · 울산대학교 대외협력팀<br>
    Tel 052-259-2066 &nbsp;|&nbsp; Fax 052-224-2062 &nbsp;|&nbsp; E-mail ysj21@ulsan.ac.kr
    </div>
    """,
    unsafe_allow_html=True,
)