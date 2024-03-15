import streamlit as st
from streamlit_folium import folium_static
from car_park_module import *

# 데이터 불러오기
data = load_data()

# 인터페이스 구성
select_sido = st.sidebar.selectbox("시도", sido_list)
select_gu = select_gu(select_sido)
payment_options = ["전체", "유료", "무료"]
select_payment_option = st.sidebar.radio("유료/무료", payment_options)


# 필터링된 데이터
filtered_data = data_filtering(data, select_sido, select_gu, select_payment_option)

# 필터링된 데이터 출력
st.dataframe(filtered_data)

# 지도 생성
folium_map = create_map(filtered_data, select_gu)

# Folium 지도를 Streamlit에 추가
folium_static(folium_map)
