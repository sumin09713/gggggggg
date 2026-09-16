import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 제목 및 설명
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 관객 수 변화를 탐색합니다.")

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜 열을 datetime 형식으로 변환 (YYYYMMDD -> YYYY-MM-DD)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 숫자형 컬럼 변환
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 구분선
st.divider()

# ----------------------------------------------------
# Section 1: 특정 영화의 날짜별 일관객 변화
# ----------------------------------------------------
st.header("📌 Section 1. 영화별 일별 관객수 추이")

# 영화 목록 추출 (관객수 총합 기준 내림차순 정렬)
top_movies_all = df.groupby('영화명')['일관객'].sum().sort_values(ascending=False).index.tolist()

# 셀렉트박스 (기본값: 관객수 가장 많은 영화)
selected_movie = st.selectbox(
    "조회할 영화를 선택하세요:",
    options=top_movies_all,
    index=0
)

# 선택한 영화의 데이터 필터링
movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

if not movie_df.empty:
    # Plotly 선 그래프 생성
    fig1 = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"<b>[{selected_movie}]</b> 날짜별 일관객 수 변화",
        labels={'날짜': '날짜', '일관객': '일일 관객 수'},
        markers=True
    )

    # Tooltip (hover) 설정
    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>관객수:</b> %{y:,}명<extra></extra>",
        line_color="#E50914"
    )

    # 레이아웃 디테일 설정
    fig1.update_layout(
        xaxis_title="날짜",
        yaxis_title="관객수 (명)",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # 그래프 출력
    st.plotly_chart(fig1, use_container_width=True)

    # 그래프 해석 / 알 수 있는 점 안내 공간
    st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성하세요)")

else:
    st.warning("선택한 영화의 데이터가 존재하지 않습니다.")

# 구분선
st.divider()

# ----------------------------------------------------
# Section 2: 일관객 합계 Top 5 영화 비교
# ----------------------------------------------------
st.header("📌 Section 2. 일관객 합계 TOP 5 영화 추이 비교")

# 일관객 합계 상위 5개 영화 선정
top5_movies = df.groupby('영화명')['일관객'].sum().nlargest(5).index.tolist()

# Top 5 영화 데이터 필터링
top5_df = df[df['영화명'].isin(top5_movies)].sort_values('날짜')

if not top5_df.empty:
    # Plotly 다중 선 그래프 생성
    fig2 = px.line(
        top5_df,
        x='날짜',
        y='일관객',
        color='영화명',
        title="<b>[TOP 5 영화]</b> 날짜별 일관객 수 비교",
        labels={'날짜': '날짜', '일관객': '일일 관객 수', '영화명': '영화 제목'},
        markers=True
    )

    # Tooltip (hover) 설정
    fig2.update_traces(
        hovertemplate="<b>영화:</b> %{fullData.name}<br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>관객수:</b> %{y:,}명<extra></extra>"
    )

    # 레이아웃 디테일 설정
    fig2.update_layout(
        xaxis_title="날짜",
        yaxis_title="관객수 (명)",
        hovermode="x unified",
        legend_title_text="영화 목록 (클릭하여 온/오프)",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # 그래프 출력
    st.plotly_chart(fig2, use_container_width=True)

    # 그래프 해석 / 알 수 있는 점 안내 공간
    st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성하세요)")

else:
    st.warning("TOP 5 영화 데이터를 불러올 수 없습니다.")

# 구분선
st.divider()

# ----------------------------------------------------
# Section 3: 날짜별 10위권 일관객 총합 영역 그래프 & 상위 3일 표시
# ----------------------------------------------------
st.header("📌 Section 3. 날짜별 10위권 전체 일관객 총합 추이")

# 날짜별 10위권 일관객 합계 계산
daily_total = df.groupby('날짜')['일관객'].sum().reset_index().sort_values('날짜')

if not daily_total.empty:
    # 영역 그래프 생성
    fig3 = px.area(
        daily_total,
        x='날짜',
        y='일관객',
        title="<b>[일별 박스오피스 전체]</b> 날짜별 TOP 10 영화 관객 총합 (상위 3일 표시)",
        labels={'날짜': '날짜', '일관객': 'TOP 10 관객 총합'}
    )

    fig3.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>TOP 10 총 관객수:</b> %{y:,}명<extra></extra>",
        fillcolor="rgba(229, 9, 20, 0.2)",
        line_color="#E50914"
    )

    # 일관객 합계가 가장 컸던 날 3일 추출
    top3_days = daily_total.nlargest(3, '일관객').sort_values('날짜')

    # 상위 3일 지점에 주석(Annotation) 및 마커 추가
    for rank, row in enumerate(top3_days.itertuples(), 1):
        date_str = row.날짜.strftime('%Y-%m-%d')
        val = row.일관객
        
        # 포인트 마커 추가
        fig3.add_trace(go.Scatter(
            x=[row.날짜],
            y=[val],
            mode='markers',
            marker=dict(size=10, color='crimson', symbol='diamond'),
            hoverinfo='skip',
            showlegend=False
        ))

        # 주석 텍스트 표기
        fig3.add_annotation(
            x=row.날짜,
            y=val,
            text=f"<b>TOP {rank}</b><br>{date_str}<br>({val:,.0f}명)",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="crimson",
            ax=0,
            ay=-45,
            bgcolor="white",
            bordercolor="crimson",
            borderwidth=1,
            borderpad=4,
            opacity=0.9
        )

    fig3.update_layout(
        xaxis_title="날짜",
        yaxis_title="총 관객수 (명)",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # 그래프 출력
    st.plotly_chart(fig3, use_container_width=True)

    # 그래프 해석 / 알 수 있는 점 안내 공간
    st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성하세요)")

else:
    st.warning("전체 일관객 총합 데이터를 불러올 수 없습니다.")

# 구분선
st.divider()

# ----------------------------------------------------
# Section 4: 기간 내 일관객 합계 TOP 10 영화 가로 막대그래프
# ----------------------------------------------------
st.header("📌 Section 4. 기간 내 일관객 합계 TOP 10 영화")

# 영화별 총 관객수 및 10위권 진입 날수 계산
top10_summary = df.groupby('영화명').agg(
    총관객수=('일관객', 'sum'),
    차트진입일수=('날짜', 'nunique')
).reset_index()

# 관객수 기준 TOP 10 추출
top10_summary = top10_summary.nlargest(10, '총관객수')

# 가로 막대그래프 정렬 설정
top10_summary = top10_summary.sort_values('총관객수', ascending=True)

if not top10_summary.empty:
    fig4 = px.bar(
        top10_summary,
        x='총관객수',
        y='영화명',
        orientation='h',
        custom_data=['차트진입일수'],
        title="<b>[전체 기간]</b> 일관객 합계 TOP 10 영화",
        labels={'총관객수': '총 관객 수 (명)', '영화명': '영화 제목'},
        text_auto=',.0f'
    )

    fig4.update_traces(
        hovertemplate="<b>영화명:</b> %{y}<br><b>총 관객수:</b> %{x:,}명<br><b>10위권 차트 진입일수:</b> %{customdata[0]}일<extra></extra>",
        marker_color="#E50914"
    )

    fig4.update_layout(
        xaxis_title="총 관객수 (명)",
        yaxis_title="영화 제목",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig4, use_container_width=True)
    st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성하세요)")

else:
    st.warning("TOP 10 영화 데이터를 불러올 수 없습니다.")

# 구분선
st.divider()

# ----------------------------------------------------
# Section 5: 월 x 요일별 일관객 합계 히트맵
# ----------------------------------------------------
st.header("📌 Section 5. 월 × 요일별 일관객 합계 히트맵")

# 날짜 데이터에서 월, 요일 추출
df_heatmap = df.copy()
df_heatmap['월'] = df_heatmap['날짜'].dt.month.astype(str) + "월"
df_heatmap['요일'] = df_heatmap['날짜'].dt.day_name()

# 요일 한글 변환 및 정렬 기준 설정 (월요일 -> 일요일)
day_map = {
    'Monday': '월요일',
    'Tuesday': '화요일',
    'Wednesday': '수요일',
    'Thursday': '목요일',
    'Friday': '금요일',
    'Saturday': '토요일',
    'Sunday': '일요일'
}
df_heatmap['요일'] = df_heatmap['요일'].map(day_map)

# 요일, 월 순서 정의
days_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
months_order = [f"{i}월" for i in range(1, 13)]

# 월 x 요일별 일관객 합계 피벗 테이블 생성
heatmap_pivot = df_heatmap.pivot_table(
    index='월',
    columns='요일',
    values='일관객',
    aggfunc='sum'
).reindex(index=months_order, columns=days_order).fillna(0)

if not heatmap_pivot.empty:
    fig5 = px.imshow(
        heatmap_pivot,
        labels=dict(x="요일", y="월", color="총 관객수 (명)"),
        x=days_order,
        y=months_order,
        color_continuous_scale="Reds",  # 관객이 많을수록 진한 빨간색
        title="<b>[월 × 요일]</b> 일관객 총합 히트맵",
        text_auto=',.0f'
    )

    # Tooltip (hover) 설정
    fig5.update_traces(
        hovertemplate="<b>%{y} %{x}</b><br><b>총 관객수:</b> %{z:,}명<extra></extra>"
    )

    fig5.update_layout(
        xaxis_title="요일",
        yaxis_title="월",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # 그래프 출력
    st.plotly_chart(fig5, use_container_width=True)

    # 그래프 해석 / 알 수 있는 점 안내 공간
    st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성하세요)")

else:
    st.warning("히트맵 데이터를 생성할 수 없습니다.")

# ----------------------------------------------------
# Section 6: (추가 예정 구역)
# ----------------------------------------------------
st.divider()
st.header("📌 Section 6. (추가 그래프 구역)")
st.caption("앞으로 추이/시간 관련 추가 그래프가 들어갈 공간입니다.")
