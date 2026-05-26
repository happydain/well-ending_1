import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Memoria - AI 엔딩노트 & 유언장",
    page_icon="🕯️",
    layout="wide"
)

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&display=swap');
    .main { background-color: #FDFBF7; }
    .stButton>button { background-color: #7D7461; color: white; border-radius: 20px; width: 100%; }
    h1, h2, h3 { color: #4A4439; font-family: 'Nanum+Myeongjo', serif; }
    .will-box {
        padding: 30px;
        border: 2px solid #4A4439;
        background-color: #FFFFFF;
        font-family: 'Nanum Myeongjo', serif;
        line-height: 1.8;
        color: #222;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }
    .disclaimer {
        font-size: 0.8rem;
        color: #888;
        background-color: #F0F0F0;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 세션 상태 초기화 ---
if 'ending_notes' not in st.session_state: st.session_state.ending_notes = {}
if 'timeline' not in st.session_state: st.session_state.timeline = []
if 'messages' not in st.session_state: st.session_state.messages = []
if 'will_draft' not in st.session_state: st.session_state.will_draft = ""

# --- 사이드바 ---
with st.sidebar:
    st.title("Memoria")
    menu = st.radio("메뉴 이동", ["홈", "AI 엔딩노트 작성", "나의 인생 타임라인", "법적 유언장 작성", "가족에게 남기는 편지", "AI 추모관"])
    st.divider()
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        client = OpenAI(api_key=api_key)

# --- 1. 홈 화면 ---
if menu == "홈":
    st.title("🕯️ Memoria")
    st.subheader("당신의 삶을 기록하고, 아름다운 마무리를 준비하세요.")
    st.image("https://images.unsplash.com/photo-1516410529446-2c777cb7366d?auto=format&fit=crop&q=80&w=1000", use_container_width=True)

# --- 2. AI 엔딩노트 작성 (생략/기존동일) ---
elif menu == "AI 엔딩노트 작성":
    st.title("📝 AI 엔딩노트")
    # ... 기존 코드와 동일 ...

# --- 3. 법적 유언장 작성 (NEW!) ---
elif menu == "법적 유언장 작성":
    st.title("⚖️ AI 법적 유언장 초안 작성")
    st.write("법적 효력을 갖추기 위한 필수 정보를 바탕으로 AI가 유언장 초안을 작성합니다.")
    
    with st.expander("💡 유언장 작성 팁 (법적 효력)", expanded=False):
        st.write("""
        대한민국 민법상 유언이 효력을 갖추려면 다음 중 하나의 방식을 따라야 합니다:
        1. **자필증서**: 전문을 직접 쓰고 날인 (가장 보편적)
        2. **녹음**: 성명, 날짜, 내용을 말로 남김
        3. **공정증서**: 공증인 앞에서 작성 (가장 확실함)
        4. **비밀증서 / 구수증서**
        *이 서비스는 '초안'을 만들어 드리며, 실제 효력을 위해서는 직접 수기로 작성하시거나 공증을 받으셔야 합니다.*
        """)

    with st.form("will_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("성명 (실명)")
            birth = st.date_input("생년월일", min_value=datetime(1900, 1, 1))
        with col2:
            address = st.text_input("현재 거주 주소")
            date_today = st.date_input("작성일", value=datetime.now())
        
        assets = st.text_area("상속 자산 목록 및 분배 방법 (예: 서울 아파트는 장남에게, 예금은 아내에게)")
        special_wish = st.text_area("기타 유언 (장례 방식, 기부 의사 등)")
        
        submitted = st.form_submit_button("AI 유언장 초안 생성")

    if submitted:
        if not api_key:
            st.error("OpenAI API Key가 필요합니다.")
        else:
            with st.spinner("법적 양식에 맞춰 초안을 구성 중입니다..."):
                prompt = f"""
                다음 정보를 바탕으로 대한민국 민법 양식에 적합한 정중하고 명확한 '유언장' 초안을 작성해줘.
                - 인적사항: 이름 {name}, 주소 {address}, 생년월일 {birth}
                - 자산분배: {assets}
                - 기타유지: {special_wish}
                - 작성일: {date_today}
                
                형식은 제목 '유 언 장'으로 시작하고, 각 항목을 번호를 매겨 정리할 것. 마지막에는 법적 효력을 위해 직접 수기 작성과 날인이 필요하다는 안내를 포함해줘.
                """
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.session_state.will_draft = response.choices[0].message.content

    if st.session_state.will_draft:
        st.markdown("### 📄 생성된 유언장 초안")
        st.markdown(f'<div class="will-box">{st.session_state.will_draft.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
        
        st.download_button(
            label="유언장 초안 다운로드 (.txt)",
            data=st.session_state.will_draft,
            file_name=f"will_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
        
        st.markdown("""
        <div class="disclaimer">
        ⚠️ <b>주의사항:</b> 본 서비스에서 생성된 문서는 법적 참고용 초안입니다. 
        대한민국 법상 자필증서 유언이 효력을 가지려면 반드시 <b>전문을 직접 손으로 쓰시고(자필), 주소, 성명을 적은 뒤 도장(날인)</b>을 찍으셔야 합니다.
        </div>
        """, unsafe_allow_html=True)

# --- 4. 나머지 메뉴 (기존과 동일하게 유지) ---
elif menu == "나의 인생 타임라인":
    st.title("⏳ 인생 타임라인")
    # ... (기존 코드)

elif menu == "가족에게 남기는 편지":
    st.title("✉️ 마지막 메시지")
    # ... (기존 코드)

elif menu == "AI 추모관":
    st.title("🕯️ 온택트 추모관")
    # ... (기존 코드)
