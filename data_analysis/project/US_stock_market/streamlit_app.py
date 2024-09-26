import streamlit as st  # Streamlit을 사용한 웹 대시보드를 만들기 위한 라이브러리

from dataloader import TickerLoader  # 데이터 로더 클래스
from model import Model  # 인사이트 도출을 위한 모델 클래스

import os  # 파일 경로 탐색을 위한 라이브러리

# 세션 상태에서 ticker 값을 False로 초기화
st.session_state["ticker"] = False

# 제목을 표시
st.write("# 📈Nasdaq Stock Market DashBoard")

# 최신 데이터 날짜를 불러와 표시
latest_day = "-".join(os.listdir("./data")[0].split("_")[1:]).split(".")[0]
st.write(f"""
- **Period: first_day - {latest_day}**
         """)

# 구분선
st.write("---")

# 데이터 로드를 위한 메시지 출력
st.write(f"### Data load")

# 데이터 로더 객체 생성 및 데이터 로드
tl = TickerLoader()
data = tl.get_data(min_days=2500, streamlit_tqdm=True)  # 최소 2500일 이상의 데이터 로드

# 사용자로부터 ticker를 입력받음 (기본값은 'NVDA')
st.session_state["ticker"] = st.text_input("ticker input", "NVDA")

# 사용자가 ticker를 입력한 경우 실행
if st.session_state["ticker"]:
    # 사용자가 입력한 ticker에 해당하는 데이터 필터링
    chart_data = data.query(f"ticker == '{st.session_state["ticker"]}'")
    
    # 구분선
    st.write("---")
    
    # 지표 (Indicator) 섹션 표시
    st.write("### Indicator")
    
    # 사용될 보조 지표들 정의
    indi_cols = ["SMA_20", "SMA_200", "RSI_14", "MACD", "MACD_signal"]
    
    # 5개의 열로 지표를 표시할 공간 생성
    cols = st.columns(5)
    
    # 마지막 2개의 row에서 각 지표의 현재 값과 전 값의 차이를 계산
    last_rows = chart_data.tail(2)[indi_cols]
    for i in range(len(indi_cols)):
        with cols[i]:
            # 지표 이름과 현재 값, 변화량을 계산 및 표시
            name = indi_cols[i]
            now_value = round(last_rows.iloc[-1][indi_cols[i]], 4)  # 현재 값
            diff_value = round(last_rows.iloc[-2][indi_cols[i]] - now_value, 4)  # 변화량
            cols[i].metric(
                name,
                now_value,
                diff_value
            )
    
    # 구분선
    st.write("---")
    
    # 차트 (Chart) 섹션 표시
    st.write("### Chart")
    
    # 126일 동안의 High, Low, SMA_20, SMA_100 데이터를 시각화
    st.line_chart(chart_data[["High", "Low", "SMA_20", "SMA_100"]].iloc[-126:])
    
    # 구분선
    st.write("---")
    
    # 인사이트 (Insight) 섹션 표시
    st.write("### Insight")
    
    # 모델을 사용하여 인사이트를 도출 (지표 분석)
    with st.spinner("Thinking... plz wait"):
        insight = Model(chart_data).get_insight()  # 모델을 사용하여 인사이트 도출
        st.write(insight)  # 인사이트 출력