"""
울산대학교 온라인 기부 약정서
-------------------------------------------------
- 상단에서 '발전기금' 또는 '후원의 집'을 선택하면 해당 약정서로 화면이 전환됩니다.
- 발전기금 : 기존 개선안 + 요청 반영(납부방법 세분화, 은행/계좌 입력, 공개 옵트아웃 등)
- 후원의 집 : 업로드된 약정서(PDF) 구현(월 구좌 정기후원 + 동의 3종)

실행: streamlit run ulsan_donation_app.py   (Streamlit 1.30 이상 권장)
"""

import datetime
import streamlit as st

# ──────────────────────────────────────────────
# 기본 설정 / 브랜드 색상 / 공통 상수
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="울산대학교 기부 약정",
    page_icon="🎓",
    layout="centered",
)

# 학교 공식 브랜드 컬러가 확정되면 이 두 값만 바꾸면 전체 톤이 바뀝니다.
PRIMARY = "#00529b"        # 대표색 (네이비 블루)
PRIMARY_DARK = "#003e76"

# 일시납부 시 입금하실 울산대학교 계좌 (예금주: 울산대학교)
ULSAN_ACCOUNTS = {
    "BNK경남은행": "540-07-0174998",
    "국민은행": "661-01-0514-551",
    "농협": "1168-01-075861",
    "하나은행": "123-890251-54205",
    "신한은행": "100-014-657050",
}

# CMS 출금에 사용할 기부자 거래은행 목록
BANK_LIST = [
    "선택하세요", "국민", "신한", "우리", "하나", "농협", "기업",
    "BNK경남", "BNK부산", "카카오뱅크", "토스뱅크", "SC제일",
    "씨티", "수협", "우체국", "새마을금고", "신협", "기타",
]

st.markdown(
    f"""
    <style>
        .block-container {{ padding-top: 2.0rem; max-width: 780px; }}

        .sec-title {{
            font-size: 1.15rem; font-weight: 700; color: {PRIMARY};
            margin: 1.8rem 0 0.2rem 0; padding-bottom: 0.4rem;
            border-bottom: 2px solid {PRIMARY};
        }}
        .sec-help {{ color: #667085; font-size: 0.88rem; margin: 0.2rem 0 0.6rem 0; }}

        div.stButton > button {{
            width: 100%; height: 3rem; border: none; border-radius: 10px;
            background-color: {PRIMARY}; color: #fff; font-weight: 700;
        }}
        div.stButton > button:hover {{ background-color: {PRIMARY_DARK}; color: #fff; }}

        .info-card {{
            background: #f4f8fc; border: 1px solid #d8e6f3; border-radius: 10px;
            padding: 0.9rem 1.1rem; font-size: 0.88rem; color: #33475b; line-height: 1.65;
        }}
        .amount-chip {{
            display: inline-block; margin-top: 0.4rem; padding: 0.3rem 0.8rem;
            background: {PRIMARY}; color: #fff; border-radius: 20px; font-weight: 700;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


def section(title: str, help_text: str | None = None) -> None:
    st.markdown(f'<div class="sec-title">{title}</div>', unsafe_allow_html=True)
    if help_text:
        st.markdown(f'<div class="sec-help">{help_text}</div>', unsafe_allow_html=True)


def footer() -> None:
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:0.85rem; color:#667085; line-height:1.7;">
        <b>문의</b> · 울산대학교 대외홍보팀<br>
        Tel 052-259-2066 &nbsp;|&nbsp; Fax 052-224-2062 &nbsp;|&nbsp;
        E-mail project@ulsan.ac.kr<br>
        Homepage https://fund.ulsan.ac.kr/fund/4718
        </div>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════
# 발전기금 약정서
# ══════════════════════════════════════════════
def render_development_fund() -> None:
    # 1. 약정 내역 ─ '어디에 쓰이는가'를 먼저
    section("1. 어디에 마음을 전하시겠어요?", "기부금이 어떤 목적에 쓰일지 선택해 주세요.")
    fund_purpose = st.radio(
        "기금 용도",
        ["교육여건개선기금", "지정기금"],
        captions=[
            "대학 전반의 교육환경 개선에 두루 사용됩니다.",
            "특정 학과·연구소·장학 등 원하시는 곳에 사용됩니다.",
        ],
    )

    target_dept, target_use = "", ""
    if fund_purpose == "지정기금":
        target_dept = st.text_input(
            "지정 대상 (학과·연구소·기관명 등)",
            placeholder="예) 의과대학 / OO연구소 / OO장학금",
        )
        target_use = st.radio("사용 목적", ["장학", "교육", "연구", "시설(건축)"], horizontal=True)

    amount = st.number_input(
        "약정 금액 (원)", min_value=10_000, step=10_000, value=100_000,
        help="최소 1만 원부터 약정하실 수 있습니다.",
    )
    st.markdown(f'<span class="amount-chip">약정 금액 {amount:,.0f} 원</span>', unsafe_allow_html=True)

    with st.expander("ℹ️ 기금 용도가 궁금하신가요?"):
        st.markdown(
            """
- **교육여건개선기금** : 대학의 교육환경 개선을 위한 일반기금입니다.
- **지정기금** : 특정 학과·연구소·장학 등 기부자께서 지정하신 목적에만 사용됩니다.

> 특정인을 지정한 기부는 「상속세 및 증여세법」상 상속·증여재산으로 해석될 수 있어
> 접수가 제한될 수 있습니다.
> 자세한 내용은 대외홍보팀 발전기금 담당(052-259-2066)으로 문의해 주세요.
"""
        )

    # 2. 납부 방법
    section("2. 어떻게 납부하시겠어요?")
    pay_method = st.radio(
        "납부 방법", ["일시 납부", "정기 납부 (CMS 자동이체)", "교직원 급여공제"]
    )

    # 출력용 변수 초기화
    pay_date = None
    deposit_bank = ""
    cms_day = ""
    cms_bank = ""
    cms_holder = ""
    cms_account = ""
    end_date = None

    if pay_method == "일시 납부":
        pay_date = st.date_input("기부 예정일", value=datetime.date.today())
        deposit_bank = st.selectbox(
            "입금하실 은행 (예금주: 울산대학교)", ["선택하세요"] + list(ULSAN_ACCOUNTS.keys())
        )
        if deposit_bank in ULSAN_ACCOUNTS:
            st.info(f"입금 계좌 · {deposit_bank} {ULSAN_ACCOUNTS[deposit_bank]}  (예금주: 울산대학교)")

    elif pay_method == "정기 납부 (CMS 자동이체)":
        cms_day = st.radio("출금일 (매월)", ["매월 15일", "매월 25일"], horizontal=True)
        end_date = st.date_input(
            "납부 종료일 (언제까지 납부하시겠어요?)",
            value=datetime.date.today() + datetime.timedelta(days=365),
            min_value=datetime.date.today(),
        )
        cms_bank = st.selectbox("거래 은행 (출금 계좌)", BANK_LIST)
        c1, c2 = st.columns(2)
        with c1:
            cms_holder = st.text_input("예금주")
        with c2:
            cms_account = st.text_input("계좌번호")
        st.caption("CMS는 금융결제원을 통한 자동이체로, 직접 은행에 가지 않고 수수료 없이 납부됩니다.")

    elif pay_method == "교직원 급여공제":
        end_date = st.date_input(
            "납부 종료일 (언제까지 납부하시겠어요?)",
            value=datetime.date.today() + datetime.timedelta(days=365),
            min_value=datetime.date.today(),
        )
        st.caption("매월 급여에서 약정액이 공제됩니다. 공제 시작 월은 담당 부서에서 안내드립니다.")

    # 3. 기부자 정보
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
        cc1, cc2 = st.columns([1, 2])
        with cc1:
            zipcode = st.text_input("우편번호")
        with cc2:
            addr1 = st.text_input("주소")
        addr2 = st.text_input("상세주소")
        company = st.text_input("직장명")
        cc3, cc4 = st.columns(2)
        with cc3:
            work_dept = st.text_input("부서")
        with cc4:
            position = st.text_input("직위")

    # 4. 기부 사실 공개 (옵트아웃)
    section(
        "4. 기부 사실 공개",
        "기부 사실을 알리길 원하지 않으시는 곳에 체크해 주세요. "
        "체크하지 않은 항목은 공개에 동의하신 것으로 봅니다. (선택)",
    )
    no_disclose = st.multiselect(
        "공개를 원하지 않는 곳",
        ["대학 홈페이지·기부 책자", "교내 기사(홈페이지·소식지)", "언론 보도"],
        label_visibility="collapsed",
    )

    # 5. 개인정보 동의
    section("5. 개인정보 수집·이용 동의 *")
    st.markdown(
        """
        <div class="info-card">
        <b>· 이용 목적</b> : 기부금영수증 발급, 후원 예우 서비스(뉴스레터·행사 초청 등) 제공, 출금(CMS) 처리<br>
        <b>· 수집 항목</b><br>
        &nbsp;&nbsp;– (필수) 이름(법인명), 휴대폰, 약정·납부 정보<br>
        &nbsp;&nbsp;– (선택) 주민(사업자)등록번호, 이메일, 주소, 직장 정보<br>
        <b>· 보유 기간</b> : 관계 법령에서 정한 보존 기간까지<br>
        울산대학교 대외홍보팀은 「개인정보 보호법」 제15조 및 제24조의2에 따라
        개인정보를 수집·이용·처리합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )
    agree = st.checkbox("위 내용을 확인했으며, 개인정보 수집·이용에 동의합니다. (필수)")

    # 제출
    st.markdown("---")
    col_cancel, col_submit = st.columns([1, 2])
    with col_cancel:
        cancelled = st.button("취소", key="dev_cancel")
    with col_submit:
        submitted = st.button("약정 신청하기", key="dev_submit")

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
        if pay_method == "일시 납부" and deposit_bank not in ULSAN_ACCOUNTS:
            errors.append("입금하실 은행을 선택해 주세요.")
        if pay_method == "정기 납부 (CMS 자동이체)":
            if cms_bank in ("", "선택하세요"):
                errors.append("CMS 출금을 위해 거래 은행을 선택해 주세요.")
            if not cms_holder.strip() or not cms_account.strip():
                errors.append("CMS 출금을 위해 예금주와 계좌번호를 입력해 주세요.")
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
                st.write("- **기부 유형** : 발전기금")
                st.write(f"- **기금 용도** : {purpose_text}")
                st.write(f"- **약정 금액** : {amount:,.0f} 원")
                st.write(f"- **납부 방법** : {pay_method}")
                if pay_method == "일시 납부":
                    st.write(f"- **기부 예정일** : {pay_date:%Y-%m-%d}")
                    st.write(f"- **입금 계좌** : {deposit_bank} {ULSAN_ACCOUNTS[deposit_bank]} (예금주: 울산대학교)")
                elif pay_method == "정기 납부 (CMS 자동이체)":
                    st.write(f"- **출금일** : {cms_day}")
                    st.write(f"- **납부 종료일** : {end_date:%Y-%m-%d}")
                    st.write(f"- **출금 계좌** : {cms_bank} / 예금주 {cms_holder} / {cms_account}")
                elif pay_method == "교직원 급여공제":
                    st.write(f"- **납부 종료일** : {end_date:%Y-%m-%d}")
                st.write(f"- **기부자** : {name}")
                if no_disclose:
                    st.write(f"- **공개 비허용** : {', '.join(no_disclose)}")


# ══════════════════════════════════════════════
# 후원의 집 약정서 (업로드된 PDF 구현)
# ══════════════════════════════════════════════
def render_supporters_house() -> None:
    st.caption("매월 일정액(구좌)을 약정·납부하는 정기 후원 프로그램입니다.")

    # 1. 약정자 정보
    section("1. 약정자 정보", "세제혜택용 기부금영수증을 원하시면 등록번호를 함께 적어 주세요.")
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("상호명")
    with c2:
        rep_name = st.text_input("대표자(성명) *")

    c3, c4 = st.columns(2)
    with c3:
        biz_num = st.text_input("사업자등록번호")
    with c4:
        biz_type = st.text_input("업태 / 업종")

    need_receipt = st.checkbox("세제혜택용 기부금영수증 발급을 원합니다.")
    resident_num = ""
    if need_receipt:
        resident_num = st.text_input(
            "주민(사업자)등록번호", help="기부금영수증 발급 용도로만 사용되며 안전하게 보관됩니다."
        )

    c5, c6 = st.columns(2)
    with c5:
        tel = st.text_input("전화번호")
    with c6:
        mobile = st.text_input("휴대폰 *")
    email = st.text_input("이메일")
    address = st.text_input("주소")

    # 2. 약정 정보
    section("2. 약정 정보")
    quota_map = {
        "1구좌 (50,000원)": 50_000,
        "2구좌 (100,000원)": 100_000,
        "3구좌 (150,000원)": 150_000,
        "4구좌 (200,000원)": 200_000,
    }
    quota = st.radio("월 약정금액 (구좌)", list(quota_map.keys()) + ["기타(직접 입력)"])
    if quota == "기타(직접 입력)":
        monthly_amount = st.number_input("월 약정금액 (원)", min_value=10_000, step=10_000, value=50_000)
    else:
        monthly_amount = quota_map[quota]

    st.markdown(
        f'<span class="amount-chip">월 약정금액 {monthly_amount:,.0f} 원</span>', unsafe_allow_html=True
    )
    st.caption("※ 약정하신 금액은 울산대학교의 일반 교육여건개선기금(교육·연구·장학금 등)으로 사용됩니다.")
    start_date = st.date_input("기부 시작일", value=datetime.date.today())

    # 3. 납부 방법 (분할 납부)
    section("3. 납부 방법 (분할 납부)")
    pay_method = st.radio("납부 방법", ["CMS 자동이체", "계좌이체 (직접 자동이체)"])
    transfer_day = st.selectbox("이체일 (매월)", [f"{d}일" for d in (5, 10, 15, 20, 25)])

    cms_bank, cms_holder, cms_account = "", "", ""
    if pay_method == "CMS 자동이체":
        cms_bank = st.selectbox("거래 은행", BANK_LIST)
        d1, d2 = st.columns(2)
        with d1:
            cms_holder = st.text_input("예금주", key="sh_holder")
        with d2:
            cms_account = st.text_input("계좌번호", key="sh_account")
        st.caption(
            "CMS는 울산대학교가 금융결제원에 자동이체 출금을 의뢰하는 방법입니다. "
            "직접 은행에 가지 않고 수수료 없이 편리하게 납부됩니다."
        )
    else:
        st.info(
            "아래 울산대학교 계좌로 매월 이체일에 직접 자동이체해 주세요.\n\n"
            "거래은행 · BNK경남은행 　|　 예금주 · 울산대학교 　|　 계좌번호 · 540-07-0174998"
        )

    # 4. 동의 (3종)
    section("4. 개인정보 및 약정 동의")

    st.markdown(
        """
        <div class="info-card">
        <b>개인정보 수집·이용 및 제3자 제공</b><br>
        · 수집·이용 목적 : 기부자 관리 및 예우, CMS 자동이체<br>
        · 수집 항목 : 위 약정정보 전체<br>
        · 보유·이용 기간 : 준영구 또는 기부자 요청 시까지<br>
        · 제3자 제공 : (사)금융결제원 (CMS 자동이체 선택 시)<br>
        · 동의를 거부하실 수 있으나, 거부 시 기부금 처리 및 기부자 예우에 어려움이 있을 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )
    agree_privacy = st.radio(
        "개인정보 수집·이용 및 제3자 제공에 동의하십니까? *",
        ["동의", "미동의"], index=None, horizontal=True,
    )

    st.markdown(
        """
        <div class="info-card">
        <b>고유식별정보(주민등록번호·사업자번호 등) 수집·이용 고지</b><br>
        기부금영수증 발급을 위해 「법인세법」 및 「소득세법」에 따라 고유식별번호가 수집·이용됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )
    agree_unique = st.radio(
        "고유식별정보 수집·이용에 동의하십니까?",
        ["동의", "미동의"], index=None, horizontal=True,
    )

    st.markdown(
        """
        <div class="info-card">
        <b>기부자 예우 및 학교 소식 안내</b><br>
        감사카드·홍보책자 등 학교 소식 안내를 위해 SMS·유선전화·이메일이 발송될 수 있으며,
        기부자 DB 및 관련 책자에 기부자의 이름이 게재될 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )
    agree_promo = st.radio(
        "기부자 예우 및 학교 소식 안내에 동의하십니까?",
        ["동의", "미동의"], index=None, horizontal=True,
    )

    # 제출
    st.markdown("---")
    col_cancel, col_submit = st.columns([1, 2])
    with col_cancel:
        cancelled = st.button("취소", key="sh_cancel")
    with col_submit:
        submitted = st.button("후원 약정 신청하기", key="sh_submit")

    if cancelled:
        st.info("작성을 취소했습니다. 언제든 다시 함께해 주세요.")

    if submitted:
        errors = []
        if not rep_name.strip():
            errors.append("대표자(성명)를 입력해 주세요.")
        if not mobile.strip():
            errors.append("휴대폰 번호를 입력해 주세요.")
        if need_receipt and not resident_num.strip():
            errors.append("영수증 발급을 위해 주민(사업자)등록번호를 입력해 주세요.")
        if pay_method == "CMS 자동이체":
            if cms_bank in ("", "선택하세요"):
                errors.append("CMS 출금을 위해 거래 은행을 선택해 주세요.")
            if not cms_holder.strip() or not cms_account.strip():
                errors.append("CMS 출금을 위해 예금주와 계좌번호를 입력해 주세요.")
        if agree_privacy != "동의":
            errors.append("개인정보 수집·이용 및 제3자 제공에 동의해 주세요. (필수)")
        if need_receipt and agree_unique != "동의":
            errors.append("기부금영수증 발급을 위해 고유식별정보 수집·이용에 동의해 주세요.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.balloons()
            st.success("후원의 집 약정이 정상 접수되었습니다. 울산대학교와 함께해 주셔서 진심으로 감사합니다. 🎓")

            with st.container(border=True):
                st.markdown("#### 약정 요약")
                st.write("- **기부 유형** : 후원의 집")
                st.write(f"- **약정자** : {rep_name}" + (f" ({biz_name})" if biz_name.strip() else ""))
                st.write(f"- **월 약정금액** : {monthly_amount:,.0f} 원")
                st.write(f"- **기부 시작일** : {start_date:%Y-%m-%d}")
                st.write(f"- **납부 방법** : {pay_method} / 매월 {transfer_day}")
                if pay_method == "CMS 자동이체":
                    st.write(f"- **출금 계좌** : {cms_bank} / 예금주 {cms_holder} / {cms_account}")
                else:
                    st.write("- **이체 계좌** : BNK경남은행 540-07-0174998 (예금주: 울산대학교)")


# ══════════════════════════════════════════════
# 메인
# ══════════════════════════════════════════════
st.title("울산대학교 기부 약정")
st.write("여러분의 따뜻한 마음이 울산대학교의 내일을 만듭니다. 아래에서 기부 유형을 선택해 주세요.")

donation_type = st.radio(
    "기부 유형",
    ["발전기금", "후원의 집"],
    captions=["원하시는 목적에 일시·정기로 기부합니다.", "매월 일정액(구좌)을 정기 후원합니다."],
    horizontal=True,
)

st.divider()

if donation_type == "발전기금":
    render_development_fund()
else:
    render_supporters_house()

footer()
