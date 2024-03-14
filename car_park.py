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
        "강북구",
        "강서구",
        "관악구",
        "광진구",
        "구로구",
        "금천구",
        "노원구",
        "도봉구",
        "동대문구",
        "동작구",
        "마포구",
        "서대문구",
        "서초구",
        "성동구",
        "성북구",
        "송파구",
        "양천구",
        "영등포구",
        "용산구",
        "은평구",
        "종로구",
        "중구",
        "중랑구",
    ],
    "인천광역시": [
        "전체",
        "계양구",
        "남동구",
        "동구",
        "미추홀구",
        "부평구",
        "서구",
        "연수구",
        "중구",
        "옹진군",
        "강화군",
    ],
    "대전광역시": [
        "전체",
        "대덕구",
        "동구",
        "서구",
        "유성구",
        "중구",
    ],
    "대구광역시": [
        "전체",
        "중구",
        "남구",
        "달서구",
        "달성군",
        "동구",
        "북구",
        "서구",
        "수성구",
    ],
    "광주광역시": [
        "전체",
        "광산구",
        "남구",
        "동구",
        "북구",
        "서구",
    ],
    "울산광역시": [
        "전체",
        "남구",
        "동구",
        "북구",
        "울주군",
        "중구",
    ],
    "부산광역시": [
        "전체",
        "강서구",
        "금정구",
        "기장군",
        "남구",
        "동구",
        "동래구",
        "부산진구",
        "북구",
        "사상구",
        "사하구",
        "서구",
        "수영구",
        "연제구",
        "영도구",
        "중구",
        "해운대구",
    ],
}


def get_selected_district(selected_sido):
    if selected_sido in sido_sigungu_mapping:
        return st.sidebar.selectbox("구", sido_sigungu_mapping[selected_sido])
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
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)  # 초기 좌표를 서울로 설정


# 해당 구의 중심 좌표로 지도 이동
if selected_district != "전체":
    district_center = filtered_data[["위도", "경도"]].mean()
    m.location = [district_center["위도"], district_center["경도"]]

# 주차장 위치에 핑 찍기
for _, row in filtered_data.iterrows():
    folium.Marker([row["위도"], row["경도"]], popup=row["소재지지번주소"]).add_to(m)

# Folium Map을 Streamlit에 추가
folium_static(m)
