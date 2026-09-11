import pandas as pd
import plotly.express as px
import streamlit as st


# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("---")


# 데이터 불러오기 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)

    # 날짜 열을 datetime 형식으로 변환 (YYYYMMDD -> YYYY-MM-DD)
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")
    return df


df = load_data()


# ==========================================
# 구역 1: 개별 영화의 날짜별 일관객 변화
# ==========================================
st.header("1. 개별 영화의 날짜별 일관객 변화")

# 영화 목록 추출 (오름차순 정렬)
movie_list = sorted(df["영화명"].unique())

# 영화 선택 드롭다운
selected_movie = st.selectbox(
    "조회할 영화를 선택하세요", movie_list, key="movie_select"
)

# 선택된 영화 데이터 필터링
filtered_df = (
    df[df["영화명"] == selected_movie].sort_values("날짜").reset_index(drop=True)
)

# Plotly 선 그래프 생성
fig1 = px.line(
    filtered_df,
    x="날짜",
    y="일관객",
    title=f"<{selected_movie}> 일별 관객수 추이",
    labels={"날짜": "날짜", "일관객": "일일 관객수(명)"},
    markers=True,
)

# 마우스 호버 시 표시될 정보 설정
fig1.update_traces(
    hovertemplate="<b>날짜</b>: %{x|%Y-%m-%d}<br><b>관객수</b>: %{y:,}명<extra></extra>"
)
fig1.update_layout(hovermode="x unified")

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 설명 문구 영역
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 내용을 작성하세요)")


st.markdown("---")


# ==========================================
# 구역 2: 추후 그래프 추가 영역
# ==========================================
# st.header("2. 새로운 그래프 제목")
# 여기에 추가 그래프 코드를 작성하면 됩니다.
