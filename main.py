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
# 구역 2. 장르 안 영화별 총 관객 트리맵
# ------------------------------------------------------------------
st.header("2. 장르 안 영화별 총 관객")

fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체"), "genre", "movieNm"],
    values="total_audi",
)
fig_treemap.update_traces(
    hovertemplate="%{label}<br>총 관객: %{value:,}명<extra></extra>",
)
fig_treemap.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.text_area(
    "💡 이 그래프로 알 수 있는 것",
    placeholder="예: ○○ 장르 안에서는 ○○○ 한 편이 총 관객의 큰 비중을 차지한다.",
    key="insight_2",
)

st.divider()

# ------------------------------------------------------------------
# 구역 3. 총 관객 분포
# ------------------------------------------------------------------
st.header("3. 총 관객 분포")

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=20,
)
fig_hist.update_traces(
    hovertemplate="구간: %{x}<br>영화 수: %{y}편<extra></extra>",
)
fig_hist.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    xaxis_title="총 관객",
    yaxis_title="영화 수",
    bargap=0.05,
)

st.plotly_chart(fig_hist, use_container_width=True)

# 가장 영화가 몰린 구간과 최다 관객 영화를 자동으로 계산
binned = pd.cut(df["total_audi"], bins=20)
top_bin = binned.value_counts().idxmax()
top_bin_count = binned.value_counts().max()

top_movie_row = df.loc[df["total_audi"].idxmax()]

st.markdown(
    f"💡 전체 216편 중 **{top_bin_count}편**이 총 관객 "
    f"**{top_bin.left:,.0f}명 ~ {top_bin.right:,.0f}명** 구간에 몰려 있고, "
    f"총 관객이 가장 많은 영화는 **{top_movie_row['movieNm']}**"
    f"({top_movie_row['total_audi']:,.0f}명)입니다."
)

st.divider()

# ------------------------------------------------------------------
# 구역 4. 개봉일 스크린수와 총 관객의 관계
# ------------------------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객의 관계")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
)
fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객: %{y:,}명<extra></extra>",
)
fig_scatter.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객",
    legend_title_text="장르",
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.text_area(
    "💡 이 그래프로 알 수 있는 것",
    placeholder="예: 개봉일 스크린수가 많을수록 총 관객도 대체로 늘어나는 경향이 있다.",
    key="insight_4",
)

st.divider()

# ------------------------------------------------------------------
# 구역 5. 장르별 총 관객 분포 (영화 10편 이상 장르만)
# ------------------------------------------------------------------
st.header("5. 장르별 총 관객 분포")

genre_movie_counts = df["genre"].value_counts()
major_genres = genre_movie_counts[genre_movie_counts >= 10].index
df_major_genres = df[df["genre"].isin(major_genres)]

fig_box = px.box(
    df_major_genres,
    x="genre",
    y="total_audi",
    points="outliers",
    hover_name="movieNm",
)
fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객: %{y:,}명<extra></extra>",
)
fig_box.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    xaxis_title="장르",
    yaxis_title="총 관객",
)

st.plotly_chart(fig_box, use_container_width=True)

st.text_area(
    "💡 이 그래프로 알 수 있는 것",
    placeholder="예: ○○ 장르는 다른 장르보다 총 관객의 편차가 크다.",
    key="insight_5",
)

st.divider()

# ------------------------------------------------------------------
# 구역 6. 개봉일 스크린수와 총 관객, 첫 주 관객까지 (버블 그래프)
# ------------------------------------------------------------------
st.header("6. 개봉일 스크린수와 총 관객, 첫 주 관객까지")
st.caption("4번 그래프에 점 크기로 first_week_audi(첫 주 관객)를 함께 표시한 버블 그래프입니다.")

fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    size="first_week_audi",
    size_max=40,
    hover_name="movieNm",
    custom_data=["first_week_audi"],
)
fig_bubble.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{customdata[0]:,}명<extra></extra>"
    ),
)
fig_bubble.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객",
    legend_title_text="장르",
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.text_area(
    "💡 이 그래프로 알 수 있는 것",
    placeholder="예: 첫 주 관객이 많은 영화(큰 점)는 대체로 총 관객도 많은 편이다.",
    key="insight_6",
)

st.divider()

# ------------------------------------------------------------------
# 구역 7. 제작 국가 안 장르별 영화 편수 (선버스트)
# ------------------------------------------------------------------
st.header("7. 제작 국가 안 장르별 영화 편수")

nation_genre_counts = (
    df.groupby(["nation", "genre"]).size().reset_index(name="count")
)

fig_sunburst = px.sunburst(
    nation_genre_counts,
    path=["nation", "genre"],
    values="count",
)
fig_sunburst.update_traces(
    hovertemplate="%{label}<br>편수: %{value}편<extra></extra>",
)
fig_sunburst.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
)

st.plotly_chart(fig_sunburst, use_container_width=True)

st.text_area(
    "💡 이 그래프로 알 수 있는 것",
    placeholder="예: ○○ 국가 영화 중에서는 ○○ 장르가 가장 많은 편수를 차지한다.",
    key="insight_7",
)

st.divider()

# ------------------------------------------------------------------
# 구역 8. (다음 그래프를 위한 빈 자리)
# ------------------------------------------------------------------
st.header("8. 다음 그래프")
st.info("이 자리에는 다음 그래프가 추가될 예정입니다.")
