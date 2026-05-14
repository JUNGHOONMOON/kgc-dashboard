import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="KGC Brand Strategy Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# KGC 브랜드 아이덴티티를 위한 커스텀 CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-top: 4px solid #b91c1c;
    }
    div[data-testid="stMetricDelta"] > div {
        font-weight: bold;
    }
    .action-card {
        background-color: #1e293b;
        color: white;
        padding: 20px;
        border-radius: 15px;
        height: 100%;
        border-left: 5px solid #b91c1c;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 헤더 영역
col_header_1, col_header_2 = st.columns([3, 1])
with col_header_1:
    st.title("에브리타임 밸런스 마케팅 통찰 📈")
    st.caption("2026년 3월 4주차 | KGC 브랜드 전략실 실시간 대시보드")

with col_header_2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("📥 PDF 리포트 다운로드", use_container_width=True)

st.divider()

# 상단 KPI 카드 레이아웃
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="수도권 판매 성장", value="+15%", delta="전주 대비 15%↑", delta_color="normal")
    st.caption("CVS 채널 점유율 1위 달성")

with kpi2:
    st.metric(label="지방 판매 추이", value="-2%", delta="전주 대비 2%↓", delta_color="inverse")
    st.caption("대형마트 채널 정체 지속")

with kpi3:
    st.metric(label="2030 세대 비중", value="45%", delta="핵심 타겟 전환 가속")
    st.caption("리뉴얼 후 유입 급증")

with kpi4:
    st.metric(label="운동 TPO 언급량", value="+30%", delta="Hot Keyword", delta_color="normal")
    st.caption("테니스·등산 연계성 강화")

st.write("")

# 중단 차트 영역
col_chart_1, col_chart_2 = st.columns([1.2, 1])

with col_chart_1:
    st.subheader("📍 채널별 판매 기여도 분석")
    chart_data = pd.DataFrame({
        "채널": ['수도권(CVS)', '수도권(마트)', '지방(마트)', '지방(CVS)', '온라인/기타'],
        "증감률": [15, 8, -2, 1, 5]
    })
    
    fig = px.bar(
        chart_data, 
        x='채널', 
        y='증감률',
        color='증감률',
        color_continuous_scale=['#64748b', '#b91c1c'],
        text_auto=True
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_chart_2:
    st.subheader("💬 고객 리뷰 밸런스 (N=500)")
    
    # 감성 분석 바
    pos, neu, neg = 72, 18, 10
    st.write("긍정 반응 (72%)")
    st.progress(pos/100)
    st.write("중립 반응 (18%)")
    st.progress(neu/100)
    st.write("부정 반응 (10%)")
    st.progress(neg/100)
    
    st.info("**핵심 긍정:** 세련된 디자인 & 완화된 쓴맛에 대한 MZ세대 선호도 상승")
    st.warning("**핵심 부정:** 가격 인상 체감 및 패키지 개봉 편의성 개선 요구")

# 하단 전략 액션 플랜
st.write("")
st.subheader("🎯 브랜드 전략실 우선순위 액션 플랜")

plan1, plan2, plan3 = st.columns(3)

with plan1:
    st.markdown("""
        <div class="action-card">
            <h4>🏃 TPO 확장 (Comm.)</h4>
            <ul>
                <li>테니스/등산 인플루언서 협업</li>
                <li>'오운완' 패키지 마케팅 강화</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with plan2:
    st.markdown("""
        <div class="action-card">
            <h4>🏪 채널 최적화 (Sales)</h4>
            <ul>
                <li>지방 마트 '패밀리 팩' 기획</li>
                <li>CVS 타겟 시간대 프로모션</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with plan3:
    st.markdown("""
        <div class="action-card">
            <h4>📦 품질 경험 개선 (UX)</h4>
            <ul>
                <li>패키지 개봉 공정 즉시 점검</li>
                <li>프리미엄 언박싱 경험 보강</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("© 2026 KGC Brand Strategy Team. Data updated as of March 27, 2026.")
