import pandas as pd
import streamlit as st
import folium


# 예제 데이터 불러오기
def load_data():
    data = pd.read_csv("carpark.csv", encoding="euc-kr")
    data["소재지지번주소"] = data["소재지지번주소"].str.strip()
    data["요금정보"] = data["요금정보"].str.strip()
    # NaN 값 제거
    data = data.dropna(subset=["위도", "경도"])
    return data


sido_list = [
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


# "시"에 대한 "구" 선택지 가져오기
def select_gu(select_sido):
    sido_gu_mapping = {
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
    if select_sido in sido_gu_mapping:
        return st.sidebar.selectbox("구", sido_gu_mapping[select_sido])
    else:
        return "전체"


# '시도' 및 '구'에 해당하는 데이터 필터링
def data_filtering(data, select_sido, select_gu, select_payment_option):
    if select_payment_option == "전체":
        filtered_data = data[data["요금정보"].notna()]
    elif select_payment_option == "유료":
        filtered_data = data[data["요금정보"].str.contains("유료|혼합", na=False)]
    else:
        filtered_data = data[data["요금정보"].str.contains("무료", na=False)]

    if select_gu == "전체":
        filtered_data = filtered_data[
            filtered_data["소재지지번주소"].str.contains(select_sido, na=False)
        ]
    else:
        filtered_data = filtered_data[
            filtered_data["소재지지번주소"].str.contains(
                f"{select_sido} {select_gu}", na=False
            )
        ]

    return filtered_data


# 주차장 위치에 핑 찍어 지도 생성
def create_map(filtered_data, select_gu):
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)  # 초기 좌표 설정

    # 해당 구로 지도 이동
    if select_gu != "전체":
        gu_center = filtered_data[["위도", "경도"]].mean()
        m.location = [gu_center["위도"], gu_center["경도"]]
    else:
        do_center = filtered_data[["위도", "경도"]].mean()
        m.location = [do_center["위도"], do_center["경도"]]

    # 주차장 위치에 핑 찍기
    if filtered_data.empty:  # 필터링된 데이터가 없을 경우
        st.warning("선택한 조건에 해당하는 주차장이 없습니다.")
    else:
        for _, row in filtered_data.iterrows():
            icon = folium.Icon(color="blue", icon="car", prefix="fa")  # 핑 아이콘 변경
            folium.Marker(
                [row["위도"], row["경도"]], popup=row["소재지지번주소"], icon=icon
            ).add_to(m)

    return m
