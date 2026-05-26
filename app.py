import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI

# --- 페이지 설정 ---
st.set_page_config(page_title="Memoria - 디지털 엔딩 플랫폼", page_icon="🕯️", layout="wide")

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&display=swap');
    .main { background-color: #FDFBF7; }
    h1, h2, h3 { color: #4A4439; font-family: 'Nanum Myeongjo', serif; }
    .stButton>button { background-color: #7D7461; color: white; border-radius: 20px; }
    .will-box {
        padding: 30px;
        border: 2px solid #4A4439;
        background-color: #FFFFFF;
        font-family: 'Nanum Myeongjo', serif;
        line-height: 1.8;
        color: #222;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }
    .contact-card { background-color: #FFFFFF; padding: 15px; border-radius: 10px; border-left: 5px solid #7D7461; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .disclaimer { font-size: 0.8rem; color: #888; background-color: #F0F0F0; padding: 10px; border-radius: 5px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 세션 상태 초기화 ---
if 'timeline' not in st.session_state: st.session_state.timeline = []
if 'contacts' not in st.session_state: st.session_state.contacts = []
if 'will_draft' not in st.session_state: st.session_state.will_draft = ""

# --- 샘플 데이터 로드 함수 ---
def load_samples():
    st.session_state.timeline = [
        {"year": 1985, "cat": "🏫 학교/교육", "title": "대학교 졸업", "desc": "청춘의 열정이 가득했던 시절, 소중한 친구들을 만났습니다."},
        {"year": 2005, "cat": "✈️ 여행/탐험", "title": "가족 스위스 여행", "desc": "아이들과 함께 본 융프라우의 만년설은 평생의 보물입니다."},
        {"year": 2018, "cat": "📚 저서/작품", "title": "첫 수필집 발간", "desc": "'나의 소소한 일상'이라는 이름의 책을 세상에 내놓았습니다."}
    ]
    st.session_state.contacts = [
        {"name": "김철수", "relation": "죽마고우", "phone": "010-1234-5678", "msg": "덕분에 인생이 즐거웠다네. 먼저 가서 기다림세."},
        {"name": "이영희", "relation": "첫 직장 동료", "phone": "010-9876-5432", "msg": "함께 꿈을 꾸던 시절을 잊지 못할 거야."}
    ]

# --- 사이드바 메뉴 ---
with st.sidebar:
    st.title("Memoria")
    menu = st.radio("이동할 메뉴", ["홈", "인생 기록 (타임라인)", "부고 알림 연락처", "법적 유언장 작성", "AI 추모관 (미리보기)"])
    st.divider()
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        client = OpenAI(api_key=api_key)
    
    st.divider()
    if st.button("샘플 데이터 불러오기"):
        load_samples()
        st.rerun()

# --- 1. 홈 화면 ---
if menu == "홈":
    st.title("🕯️ Memoria")
    st.subheader("당신의 삶은 기록되고, 당신의 사랑은 기억됩니다.")
    st.image("https://images.unsplash.com/photo-1516410529446-2c777cb7366d?auto=format&fit=crop&q=80&w=1000", use_container_width=True)
    st.write("왼쪽 메뉴를 통해 인생의 기록을 남기고, 사후 지침을 안전하게 보관하세요.")

# --- 2. 인생 기록 (타임라인) ---
elif menu == "인생 기록 (타임라인)":
    st.title("⏳ 나의 일생 기록하기")
    with st.form("timeline_entry"):
        col1, col2 = st.columns([1, 2])
        with col1:
            year = st.number_input("연도", 1930, 2025, 2000)
            category = st.selectbox("카테고리", ["🏫 학교/교육", "🏆 직장/성과", "✈️ 여행/탐험", "📚 저서/작품", "🏠 가족/개인", "❤️ 기타"])
        with col2:
            title = st.text_input("사건명")
            description = st.text_area("상세 추억 기록")
        if st.form_submit_button("기록 추가"):
            st.session_state.timeline.append({"year": year, "cat": category, "title": title, "desc": description})
            st.success("타임라인에 추가되었습니다.")

    if st.session_state.timeline:
        st.divider()
        for item in sorted(st.session_state.timeline, key=lambda x: x['year'], reverse=True):
            with st.expander(f"[{item['year']}] {item['cat']} - {item['title']}"):
                st.write(item['desc'])

# --- 3. 부고 알림 연락처 ---
elif menu == "부고 알림 연락처":
    st.title("📞 부고를 알릴 지인 목록")
    with st.form("contact_form"):
        c_name = st.text_input("성함")
        c_relation = st.text_input("관계")
        c_phone = st.text_input("연락처")
        c_msg = st.text_area("그분에게 남기는 마지막 인사")
        if st.form_submit_button("연락처 저장"):
            st.session_state.contacts.append({"name": c_name, "relation": c_relation, "phone": c_phone, "msg": c_msg})
            st.success(f"{c_name}님의 정보가 저장되었습니다.")

    if st.session_state.contacts:
        for person in st.session_state.contacts:
            st.markdown(f"""
            <div class="contact-card">
                <b>{person['name']} ({person['relation']})</b> | 📞 {person['phone']}<br>
                <i style="color: #666;">" {person['msg']} "</i>
            </div>
            """, unsafe_allow_html=True)

# --- 4. 법적 유언장 작성 (이전 로직 그대로 유지) ---
elif menu == "법적 유언장 작성":
    st.title("⚖️ AI 법적 유언장 초안 작성")
    st.write("법적 효력을 갖추기 위한 정보를 바탕으로 AI가 정중한 초안을 작성합니다.")
    
    with st.form("will_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("성명 (실명)")
            birth = st.date_input("생년월일", min_value=datetime(1900, 1, 1))
        with col2:
            address = st.text_input("현재 거주 주소")
            date_today = st.date_input("작성일", value=datetime.now())
        
        assets = st.text_area("상속 자산 목록 및 분배 방법 (예: 아파트는 배우자에게, 예금은 자녀들에게 등분)")
        special_wish = st.text_area("기타 유언 (장례 방식, 기부 의사 등)")
        
        submitted = st.form_submit_button("AI 유언장 초안 생성")

    if submitted:
        if not api_key:
            st.error("사이드바에 OpenAI API Key를 입력해주세요.")
        else:
            with st.spinner("법률 서식에 맞춰 초안을 작성 중입니다..."):
                prompt = f"""
                다음 정보를 바탕으로 대한민국 민법 양식에 적합한 정중하고 명확한 '유언장' 초안을 작성해줘.
                - 인적사항: 이름 {name}, 주소 {address}, 생년월일 {birth}
                - 자산분배: {assets}
                - 기타유지: {special_wish}
                - 작성일: {date_today}
                형식은 제목 '유 언 장'으로 시작하고 번호를 매겨서 정리해줘.
                """
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.session_state.will_draft = response.choices[0].message.content

    if st.session_state.will_draft:
        st.markdown(f'<div class="will-box">{st.session_state.will_draft.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
        st.download_button(label="유언장 다운로드 (.txt)", data=st.session_state.will_draft, file_name="will_draft.txt")
        st.markdown('<div class="disclaimer">⚠️ 주의: 법적 효력을 위해 반드시 전문을 자필로 작성하고 날인하시기 바랍니다.</div>', unsafe_allow_html=True)

# --- 5. AI 추모관 미리보기 ---
elif menu == "AI 추모관 (미리보기)":
    st.title("🕯️ 고인을 추억하는 공간")
    tab1, tab2 = st.tabs(["🌟 인생의 발자취", "🙏 부고 안내"])
    
    with tab1:
        if st.session_state.timeline:
            for item in sorted(st.session_state.timeline, key=lambda x: x['year']):
                st.markdown(f"### {item['year']}년 - {item['title']}")
                st.caption(item['cat'])
                st.write(item['desc'])
                st.divider()
        else: st.write("아직 기록이 없습니다.")

    with tab2:
        st.subheader("연락드릴 지인 명단")
        for p in st.session_state.contacts:
            st.write(f"- {p['name']} ({p['phone']}) : {p['relation']}")
