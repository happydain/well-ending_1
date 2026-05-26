import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI

# --- 페이지 설정 ---
st.set_page_config(page_title="Memoria - 디지털 엔딩노트", page_icon="🕯️", layout="wide")

# --- 스타일링 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&display=swap');
    .main { background-color: #FDFBF7; }
    h1, h2, h3 { color: #4A4439; font-family: 'Nanum Myeongjo', serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #F1EDE4; border-radius: 10px 10px 0 0; padding: 10px; }
    .contact-card { background-color: #FFFFFF; padding: 15px; border-radius: 10px; border-left: 5px solid #7D7461; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 세션 상태 초기화 ---
if 'timeline' not in st.session_state: st.session_state.timeline = []
if 'contacts' not in st.session_state: st.session_state.contacts = []
if 'ending_notes' not in st.session_state: st.session_state.ending_notes = {}

# --- 샘플 데이터 함수 ---
def load_samples():
    st.session_state.timeline = [
        {"year": 1985, "cat": "🏫 학교", "title": "서울대학교 졸업", "desc": "경제학 전공, 소중한 친구들을 만남"},
        {"year": 1992, "cat": "🏆 성과", "title": "첫 직장 승진", "desc": "해외 영업팀 과장 승진, 나만의 커리어를 쌓기 시작"},
        {"year": 2005, "cat": "✈️ 여행", "title": "가족과 함께한 스위스", "desc": "인터라켄에서 본 만년설은 잊을 수 없음"},
        {"year": 2015, "cat": "📚 저서", "title": "나의 삶, 나의 길 출판", "desc": "60세 기념 자서전 독립 출판"},
    ]
    st.session_state.contacts = [
        {"name": "김철수", "relation": "고향 친구", "phone": "010-1234-5678", "msg": "내 마지막 술친구, 고마웠네."},
        {"name": "이영희", "relation": "첫 직장 동기", "phone": "010-9876-5432", "msg": "함께 치열했던 젊은 날을 기억해줘."}
    ]

# --- 사이드바 메뉴 ---
with st.sidebar:
    st.title("Memoria")
    menu = st.radio("이동할 메뉴", ["홈", "인생 기록 (타임라인)", "부고 알림 연락처", "법적 유언장", "AI 추모관 미리보기"])
    st.divider()
    if st.button("샘플 데이터 불러오기"):
        load_samples()
        st.rerun()

# --- 1. 홈 화면 ---
if menu == "홈":
    st.title("🕯️ 당신의 인생을 아름답게 갈무리하세요")
    st.write("Memoria는 단순한 유언장이 아닌, 당신의 살아온 흔적을 남기는 공간입니다.")
    st.image("https://images.unsplash.com/photo-1490122417551-6ee9691429d0?auto=format&fit=crop&q=80&w=1000")

# --- 2. 인생 기록 (타임라인 강화형) ---
elif menu == "인생 기록 (타임라인)":
    st.title("⏳ 나의 일생 기록하기")
    st.write("주요 사건, 성과, 여행, 창작물 등을 연도별로 기록하세요.")
    
    with st.form("timeline_entry"):
        col1, col2 = st.columns([1, 2])
        with col1:
            year = st.number_input("연도", 1930, 2025, 2000)
            category = st.selectbox("카테고리", ["🏫 학교/교육", "🏆 직장/성과", "✈️ 여행/탐험", "📚 저서/작품", "🏠 가족/개인", "❤️ 기타"])
        with col2:
            title = st.text_input("사건명 (예: 대학교 입학, 첫 책 출간)")
            description = st.text_area("상세 추억 기록")
        
        if st.form_submit_button("기록 추가"):
            st.session_state.timeline.append({"year": year, "cat": category, "title": title, "desc": description})
            st.success("새로운 기록이 타임라인에 저장되었습니다.")

    # 타임라인 표시
    if st.session_state.timeline:
        st.divider()
        df = pd.DataFrame(st.session_state.timeline).sort_values(by="year", ascending=False)
        for _, row in df.iterrows():
            with st.expander(f"[{row['year']}] {row['cat']} - {row['title']}"):
                st.write(row['desc'])

# --- 3. 부고 알림 연락처 (NEW!) ---
elif menu == "부고 알림 연락처":
    st.title("📞 마지막 소식을 전할 사람들")
    st.write("사망 시 나의 소식을 우선적으로 알려야 할 명단을 작성하세요.")
    
    with st.form("contact_form"):
        c_name = st.text_input("성함")
        c_relation = st.text_input("관계 (예: 동창, 조카, 오랜 친구)")
        c_phone = st.text_input("연락처 (전화번호 또는 이메일)")
        c_msg = st.text_area("그분에게 남기는 마지막 짧은 인사")
        
        if st.form_submit_button("연락처 저장"):
            st.session_state.contacts.append({"name": c_name, "relation": c_relation, "phone": c_phone, "msg": c_msg})
            st.success(f"{c_name}님의 정보가 안전하게 저장되었습니다.")

    if st.session_state.contacts:
        st.subheader("📋 저장된 명단")
        for person in st.session_state.contacts:
            st.markdown(f"""
            <div class="contact-card">
                <b>{person['name']} ({person['relation']})</b> | 📞 {person['phone']}<br>
                <i style="color: #666;">" {person['msg']} "</i>
            </div>
            """, unsafe_allow_html=True)

# --- 4. 법적 유언장 ---
elif menu == "법적 유언장":
    st.title("⚖️ 유언장 초안 작성")
    st.info("이곳은 재산 분배 및 법적 요구사항을 정리하는 공간입니다.")
    # (이전 코드의 유언장 생성 로직 배치)

# --- 5. AI 추모관 미리보기 (통합) ---
elif menu == "AI 추모관 미리보기":
    st.title("🕯️ 고인의 디지털 추모관")
    st.write("가족과 지인들이 보게 될 최종 화면입니다.")
    
    tab1, tab2, tab3 = st.tabs(["🌟 인생의 발자취", "✉️ 남긴 메시지", "🙏 부고 및 안내"])
    
    with tab1:
        if st.session_state.timeline:
            for item in sorted(st.session_state.timeline, key=lambda x: x['year']):
                st.markdown(f"**{item['year']}년** - {item['cat']}")
                st.markdown(f"#### {item['title']}")
                st.write(item['desc'])
                st.divider()
        else:
            st.write("아직 기록된 인생 타임라인이 없습니다.")

    with tab2:
        st.subheader("지인들에게 남긴 마지막 인사")
        for p in st.session_state.contacts:
            if p['msg']:
                st.markdown(f"**{p['name']} ({p['relation']}) 님께:**")
                st.info(p['msg'])

    with tab3:
        st.subheader("연락 주실 곳")
        st.write("부고를 받으실 분들 목록입니다 (시스템 자동 발송)")
        for p in st.session_state.contacts:
            st.write(f"- {p['name']} ({p['phone']})")
