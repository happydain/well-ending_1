import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Memoria - AI 엔딩노트 & 추모 플랫폼",
    page_icon="🕯️",
    layout="wide"
)

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #FDFBF7; }
    .stButton>button { background-color: #7D7461; color: white; border-radius: 20px; }
    h1, h2, h3 { color: #4A4439; font-family: 'Nanum Myeongjo', serif; }
    .memorial-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
        border: 1px solid #EAE2D6;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 세션 상태 초기화 (데이터 저장용) ---
if 'ending_notes' not in st.session_state:
    st.session_state.ending_notes = {}
if 'timeline' not in st.session_state:
    st.session_state.timeline = []
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- 사이드바 메뉴 ---
with st.sidebar:
    st.title("Memoria")
    st.info("당신의 삶을 기록하고, 아름다운 마무리를 준비하세요.")
    menu = st.radio("메뉴 이동", ["홈", "AI 엔딩노트 작성", "나의 인생 타임라인", "가족에게 남기는 편지", "AI 추모관 (미리보기)"])
    
    st.divider()
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        client = OpenAI(api_key=api_key)

# --- 1. 홈 화면 ---
if menu == "홈":
    st.title("🕯️ Memoria")
    st.subheader("당신의 삶은 기록되고, 당신의 사랑은 기억됩니다.")
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 왜 엔딩노트가 필요한가요?
        - **존엄한 마무리**: 내 의지가 담긴 장례와 유산 정리
        - **남겨진 이들을 위한 배려**: 갑작스러운 이별 시 행정적 혼란 방지
        - **삶의 재발견**: 기록을 통해 현재의 소중함 확인
        """)
    with col2:
        st.image("https://images.unsplash.com/photo-1506784983877-45594efa4cbe?auto=format&fit=crop&q=80&w=500", caption="기록의 가치")

# --- 2. AI 엔딩노트 작성 ---
elif menu == "AI 엔딩노트 작성":
    st.title("📝 AI 엔딩노트 인터뷰")
    st.write("AI가 질문을 통해 당신의 마지막 페이지 작성을 돕습니다.")
    
    if not api_key:
        st.warning("사이드바에 OpenAI API Key를 입력해주세요.")
    else:
        question_category = st.selectbox("항목 선택", ["장례 방식", "재정 정보", "디지털 자산 정리", "반려동물 케어"])
        
        user_input = st.text_area(f"'{question_category}'에 대해 평소 생각하신 점을 자유롭게 적어주세요.")
        
        if st.button("AI와 정리하기"):
            with st.spinner("생각을 정리 중입니다..."):
                prompt = f"사용자가 {question_category}에 대해 다음과 같이 말했습니다: '{user_input}'. 이를 바탕으로 유족들이 명확히 알 수 있도록 엔딩노트 형식으로 정중하게 요약해줘."
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                st.session_state.ending_notes[question_category] = result
                st.success("기록되었습니다!")
        
        if question_category in st.session_state.ending_notes:
            st.markdown(f"**현재 저장된 내용:**")
            st.info(st.session_state.ending_notes[question_category])

# --- 3. 인생 타임라인 ---
elif menu == "나의 인생 타임라인":
    st.title("⏳ 인생 타임라인")
    
    with st.form("timeline_form"):
        year = st.number_input("연도", min_value=1900, max_value=2025, value=2000)
        event = st.text_input("사건/기억")
        desc = st.text_area("상세 내용")
        if st.form_submit_button("추가하기"):
            st.session_state.timeline.append({"year": year, "event": event, "desc": desc})
    
    if st.session_state.timeline:
        df = pd.DataFrame(st.session_state.timeline).sort_values(by="year")
        for idx, row in df.iterrows():
            with st.expander(f"{row['year']}년 - {row['event']}"):
                st.write(row['desc'])

# --- 4. 가족에게 남기는 편지 ---
elif menu == "가족에게 남기는 편지":
    st.title("✉️ 마지막 메시지")
    recipient = st.text_input("수신인 (예: 딸에게, 아내에게)")
    message = st.text_area("전하고 싶은 마음")
    
    if st.button("메시지 봉인하기"):
        st.session_state.messages.append({"to": recipient, "msg": message, "date": datetime.now().strftime("%Y-%m-%d")})
        st.success("메시지가 안전하게 보관되었습니다. 설정된 조건 시 전달됩니다.")

# --- 5. AI 추모관 미리보기 ---
elif menu == "AI 추모관 (미리보기)":
    st.title("🕯️ 온택트 추모관")
    st.write("사후에 가족들에게 보여질 공간의 예시입니다.")
    
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://via.placeholder.com/300x400", caption="고인의 모습 (샘플)")
        st.markdown("### 故 홍길동 (1960 - 2024)")
    
    with col2:
        st.markdown("#### 📜 삶의 요약")
        st.write("따뜻한 남편이었으며, 평생 교육자로서 헌신했던 사람입니다.")
        
        tab1, tab2 = st.tabs(["추모사", "남긴 편지"])
        with tab1:
            if st.session_state.ending_notes:
                for cat, content in st.session_state.ending_notes.items():
                    st.write(f"**{cat}에 대한 유지:**")
                    st.write(content)
            else:
                st.write("등록된 유지(遺旨)가 없습니다.")
        
        with tab2:
            for m in st.session_state.messages:
                st.markdown(f"""
                <div class="memorial-card">
                    <b>To. {m['to']}</b><br>
                    <small>{m['date']}</small><br><br>
                    {m['msg']}
                </div>
                """, unsafe_allow_html=True)

# --- 푸터 ---
st.markdown("---")
st.caption("Memoria © 2024 - 당신의 삶의 마지막 기록을 돕습니다.")
