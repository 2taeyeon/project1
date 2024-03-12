# 맨처음 ui부터 만들기
# 지역별로 나누고 광역시는 구로 나누어서 찾게하기
# 다 선택하면 지도를 띄우고 핑찍어서 보이게 하기


import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium

# 예제 데이터 불러오기
data = pd.read_csv("carpark.csv", encoding="euc-kr")

# 소재지지번주소 컬럼에 대한 정제 작업 추가
data["소재지지번주소"] = data["소재지지번주소"].str.strip()

# NaN 값을 가진 행 제거
data = data.dropna(subset=["위도", "경도"])

# 사용자가 선택할 수 있는 '시도' 리스트 생성
sido_list = [
    "전체",
    "서울특별시",
    "인천광역시",
    "대전광역시",
    "대구광역시",
    "광주광역시",
    "울산광역시",
    "부산광역시",
    "세종특별자치시",
    "경기도",
    "강원특별자치도",
    "강원도",
    "충청북도",
    "충청남도",
    "전라북도",
    "전북특별자치도",
    "전라남도",
    "경상북도",
    "경상남도",
    "제주특별자치도",
]

# 각 '시도'에 해당하는 '시군구' 옵션을 매핑한 딕셔너리 정의
sido_sigungu_mapping = {
    "서울특별시": [
        "전체",
        "강남구",
        "강동구",
        # ... 이하 생략 ...
    ],
    "인천광역시": [
        "전체",
        "계양구",
        # ... 이하 생략 ...
    ],
    "대전광역시": [
        "전체",
        "동구",
        # ... 이하 생략 ...
    ],
    "대구광역시": [
        "전체",
        "남구",
        # ... 이하 생략 ...
    ],
    "광주광역시": [
        "전체",
        "동구",
        # ... 이하 생략 ...
    ],
    "울산광역시": [
        "전체",
        "남구",
        # ... 이하 생략 ...
    ],
    "부산광역시": [
        "전체",
        "남구",
        # ... 이하 생략 ...
    ],
}


def get_selected_district(selected_sido):
    if selected_sido in sido_sigungu_mapping:
        return st.sidebar.selectbox(
            "구", ["전체"] + sido_sigungu_mapping[selected_sido]
        )
    else:
        return "전체"


# 사용자가 선택한 '시도' 및 '구'에 해당하는 데이터를 필터링
selected_sido = st.sidebar.selectbox("시도", sido_list)
selected_district = get_selected_district(selected_sido)

# 선택한 '시도'와 '구'에 해당하는 데이터를 DataFrame으로 표시
if selected_district == "전체":
    filtered_data = data[data["소재지지번주소"].str.contains(selected_sido, na=False)]
else:
    filtered_data = data[
        data["소재지지번주소"].str.contains(
            f"{selected_sido} {selected_district}", na=False
        )
    ]

filtered_data["소재지지번주소"].fillna("NaN", inplace=True)

# 선택한 '시도' 및 '구'에 해당하는 데이터를 DataFrame으로 표시
st.dataframe(filtered_data)

# Folium Map 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=12)  # 초기 좌표를 대구로 설정

# 해당 구의 중심 좌표로 지도 이동
if selected_district != "전체":
    district_center = filtered_data[["위도", "경도"]].mean()
    m.location = [district_center["위도"], district_center["경도"]]

# 주차장 위치에 핑 찍기
for _, row in filtered_data.iterrows():
    folium.Marker([row["위도"], row["경도"]], popup=row["소재지지번주소"]).add_to(m)

# Folium Map을 Streamlit에 추가
folium_static(m)
