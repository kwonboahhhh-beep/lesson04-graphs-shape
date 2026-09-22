import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # openDt: 여덟 자리 숫자(YYYYMMDD) -> 날짜형
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d")

    # genre: 세로막대(|) 기호로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    return df


df = load_data()

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("최근 1년간 박스오피스 10위권에 든 영화 216편의 데이터를 살펴봅니다.")

st.divider()

# ------------------------------------------------------------------
# 구역 1. 장르별 영화 편수
# ------------------------------------------------------------------
st.header("1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
)
fig_genre.update_traces(
    textinfo="label+percent",
    hovertemplate="%{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig_genre.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    legend_title_text="장르",
)

st.plotly_chart(fig_genre, use_container_width=True)

st.text_area(
    "💡 이 그래프로 알 수 있는 것",
    placeholder="예: 최근 1년간 박스오피스 상위권 영화 중 가장 많은 편수를 차지한 장르는 ○○이다.",
    key="insight_1",
)

st.divider()

# ------------------------------------------------------------------
# 구역 2. (다음 그래프를 위한 빈 자리)
# ------------------------------------------------------------------
st.header("2. 다음 그래프")
st.info("이 자리에는 다음 그래프가 추가될 예정입니다.")
