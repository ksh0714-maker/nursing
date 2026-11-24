import streamlit as st
import pandas as pd

# 1. 데이터 구조 (리스트): 증상별 필수 간호 중재 목록 정의
fever_care = [
    ["미온수 마사지", "상", "겨드랑이·사타구니 위주 닦아주기"],
    ["수분 섭취 권장", "중", "탈수 예방을 위한 미지근한 물 공급"],
    ["해열제 투여 확인", "하", "의사 처방에 따른 정량 투약 여부 확인"]
]

hypotension_care = [
    ["하지 거상 체위", "상", "누운 상태에서 다리를 심장보다 높게 올리기"],
    ["활력징후 재측정", "상", "5~10분 간격으로 혈압 및 맥박 변화 관찰"],
    ["수액 공급 준비", "중", "정맥 주사 경로 확보 및 의료진 보고"]
]

dyspnea_care = [
    ["반좌위(파울러씨 체위)", "상", "상체를 45~60도 세워 폐 확장 돕기"],
    ["산소포화도 측정", "상", "맥박산소측정기로 SpO2 수치 확인"],
    ["의복 느슨하게 하기", "중", "목과 가슴 부위의 조이는 옷 풀어주기"]
]

# 2. 함수 (def): 증상과 체온을 매개변수로 받아 위험도 점수와 안내 문구 리턴
def check_vital(symptom, temp):
    risk_score = 40  # 기본 정상 위험도 점수
    
    # 체온(temp) 정상/비정상 범위 판별
    if temp < 36.0:
        risk_score += 20
        temp_status = "저체온 주의(36.0°C 미만)"
    elif temp >= 38.5:
        risk_score += 25
        temp_status = "고위험 고열(38.5°C 이상)"
    elif temp >= 37.5:
        risk_score += 10
        temp_status = "미열 상태(37.5°C 이상)"
    else:
        temp_status = "정상 체온 범위(36.0~37.4°C)"

    # 조건문 (if-elif-else): 증상 및 체온 조합 판별
    if symptom == "고열":
        if temp < 37.5:
            message = f"ℹ️ 현재 체온은 {temp}°C({temp_status})로, 고열 상태가 아닙니다. 체온을 다시 확인하세요."
        elif temp >= 38.5:
            risk_score += 15
            message = f"⚠️ {temp_status}입니다. 즉각적인 체온 조절 간호 중재가 필요합니다."
        else:
            message = f"현재 {temp_status}입니다. 주기적인 체온 관찰이 필요합니다."
            
    elif symptom == "저혈압":
        risk_score += 20
        if temp < 36.0:
            risk_score += 15
            message = f"⚠️ 저혈압과 {temp_status}이 동반되었습니다. 쇼크 예방을 위한 즉각 조치가 필요합니다."
        else:
            message = f"혈압 저하가 감지되었습니다. ({temp_status}) 체위 변경 및 지속적인 혈압 모니터링이 필요합니다."
            
    else:  # 호흡곤란
        risk_score += 25
        if temp >= 38.0:
            risk_score += 15
            message = f"⚠️ 발열을 동반한 호흡곤란({temp_status})입니다. 기도 확보 및 산소 공급이 시급합니다."
        else:
            message = f"호흡곤란 증상이 있습니다. ({temp_status}) 상체를 높여주고 호흡 양상을 관찰하세요."
            
    return risk_score, message

# --- 화면 UI 구성 ---
st.title("🩺 맞춤형 환자 바이탈 체크 및 간호 가이드")
st.write("환자의 주요 증상과 체온을 입력하면 위험도와 초기 간호 중재 방법을 안내합니다.")

symptom_input = st.selectbox(
    "(1) 주요 증상 선택",
    ["고열", "저혈압", "호흡곤란"]
)

temp_input = st.slider(
    "(2) 체온 입력(°C)",
    min_value=35.0,
    max_value=41.0,
    value=37.5,
    step=0.1
)

# 버튼 클릭 시 결과 출력
if st.button("상태 분석하기"):
    st.divider()
    st.subheader("[결과 출력 화면]")
    
    score, warning_msg = check_vital(symptom_input, temp_input)
    
    if "⚠️" in warning_msg:
        st.error(warning_msg)
    elif "ℹ️" in warning_msg:
        st.info(warning_msg)
    else:
        st.warning(warning_msg)
        
    st.metric(label="환자 위험도 점수", value=f"{score}점", delta="정상 기준(40점) 대비")

    if symptom_input == "고열":
        selected_list = fever_care
    elif symptom_input == "저혈압":
        selected_list = hypotension_care
    else:
        selected_list = dyspnea_care

    # 반복문 (for): 간호 중재 리스트를 테이블 데이터로 변환
    table_data = []
    for item in selected_list:
        table_data.append({
            "중재 항목": item[0],
            "우선순위": item[1],
            "세부 간호 내용": item[2]
        })

    st.write("**📋 필수 간호 중재 목록**")
    df = pd.DataFrame(table_data)
    st.table(df)
