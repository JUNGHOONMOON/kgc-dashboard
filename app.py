import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(page_title="KGC 브랜드전략실 - 대시보드", layout="wide")

# --- [데이터 로드 섹션] ---
# 사용자님의 시트 ID (공유 설정이 되어 있어야 합니다)
SHEET_ID = "1vMwTPja0QsD6FA9sPy7W8zoA_40mR4M93F2-1caFWrI"

# 구글 시트 URL (Secrets에 저장했다면 st.secrets["gsheet_url"]로 대체 가능)
KPI_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=60)  # 1분간 캐시 유지
def load_data(url):
    return pd.read_csv(url)

try:
    # 1. KPI 데이터 로드 (image_bcd3fe.png의 데이터가 들어있는 시트)
    df_raw = load_data(KPI_URL)
    
    # 2. KPI 카드용 데이터 분리 (상위 4개 행)
    df_kpi = df_raw.head(4)

    # 3. AI 요약 내용 추출 (A7 셀 위치: index 5, column 0)
    # 데이터가 부족할 경우를 대비해 예외 처리 포함
    if len(df_raw) >= 6:
        ai_summary = df_raw.iloc[5, 0]
    else:
        ai_summary = "현재 구글 시트에서 데이터를 분석 중입니다. 잠시만 기다려주세요."

except Exception as e:
    st.error(f"⚠️ 데이터를 불러올 수 없습니다. 시트 설정을 확인해주세요. ({e})")
    st.stop()

# -----------------------

# 2. 커스텀 CSS (KGC 브랜드 컬러 반영)
st.markdown("""
    <style>
    .kpi-value { font-size: 28px; font-weight: bold; color: #A6192E; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #f0f2f6; }
    [data-testid="stMetricDelta"] > div:nth-child(2) { font-size: 14px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. 헤더 영역
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title("📈 에브리타임 밸런스 마케팅 대시보드")
    st.markdown("**2026년 3월 4주차 | 리뉴얼 제품 판매 및 여론 분석**")
with col_header2:
    st.write("") 
    st.info("👤 **팀장: 인선미** (Brand Strategy)")

st.divider()

# 4. KPI 카드 영역 (image_bcd3fe.png의 데이터 기반)
# 4개의 지표(수도권 판매량, 핵심 타겟층, 스포츠 키워드, 긍정 리뷰)를 가로로 배치
kpi_cols = st.columns(len(df_kpi))
for i, col in enumerate(kpi_cols):
    # 값에 따라 색상이나 포맷을 조정할 수 있습니다.
    label_text = df_kpi.iloc[i]['label']
    value_text = str(df_kpi.iloc[i]['value'])
    delta_text = df_kpi.iloc[i]['delta']
    
    # delta_color 설정 (필요에 따라 조정 가능)
    col.metric(
        label=label_text, 
        value=value_text, 
        delta=delta_text,
        delta_color="normal"
    )

st.markdown("<br>", unsafe_allow_html=True)

# 5. 시각화 및 분석 영역
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 항목별 상세 수치 분석")
    # 그래프를 위해 value에서 % 제거 후 숫자로 변환
    df_plot = df_kpi.copy()
    df_plot['numeric_value'] = pd.to_numeric(df_plot['value'].astype(str).str.replace('%', ''), errors='coerce')
    
    fig = px.bar(
        df_plot, x="label", y="numeric_value", text="value",
        color="label", color_discrete_sequence=['#A6192E', '#C5A059', '#94a3b8', '#475569']
    )
    fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=0, r=0), height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("💡 팀장 전략 제언 (Action Items)")
    st.info("""
    1. **아웃도어 마케팅:** '스포츠 키워드' 언급 증가에 따른 테니스/등산 커뮤니티 연계 캠페인 강화
    2. **타겟 확장:** 핵심 타겟층(4050) 외 사회초년생 구매 비중 증가에 따른 타겟팅 광고 세분화
    3. **리뷰 관리:** 긍정 리뷰 내 '패키지/맛 만족도' 키워드를 상세페이지 마케팅 포인트로 활용
    """)

with col_right:
    st.subheader("🔥 트렌드 키워드")
    st.markdown("`#사회초년생` `#테니스` `#오운완` `#선물추천` `#등산` `#에너지부스터`")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📌 Today's Summary")
    # 구글 시트 A7 셀의 내용을 표시
    st.warning(ai_summary)
    st.caption("※ 구글 시트의 마케팅 데이터를 Gemini AI가 실시간 분석한 결과입니다.")
    
    st.markdown("---")
    st.subheader("💬 실시간 고객 VOC")
    st.success("**🟢 Positive**\n\n- 포장이 세련되어 선물용으로 최고\n- 기존보다 쓴맛이 덜해 먹기 편함")
    st.error("**🔴 Improvement**\n\n- 리뉴얼 후 가격 접근성 고민 필요\n- 일부 패키지 개봉 시 뻑뻑함")

# 하단 푸터
st.markdown("<br><hr><center style='color: grey;'>KGC Brand Strategy Team Dashboard © 2026</center>", unsafe_allow_html=True)
