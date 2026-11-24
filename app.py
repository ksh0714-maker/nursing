# 1) 텍스트 메시지 출력 (경고 및 안내 문구)
    if "⚠️" in warning_msg:
        st.error(warning_msg)
    else:
        st.warning(warning_msg)
        
    # 2) 강조 수치(Metric) 형태로 환자 위험도 점수 표시
    st.metric(label="환자 위험도 점수", value=f"{score}점", delta="정상 기준(40점) 대비")

    # 3) 선택된 증상에 맞는 리스트 매핑
    if symptom_input == "고열":
        selected_list = fever_care
    elif symptom_input == "저혈압":
        selected_list = hypotension_care
    else:
        selected_list = dyspnea_care

    # 4) 반복문(for): 간호 중재 리스트를 순회하여 테이블 생성용 데이터로 변환
    table_data = []
    for item in selected_list:
        table_data.append({
            "중재 항목": item[0],
            "우선순위": item[1],
            "세부 간호 내용": item[2]
        })

    # 5) 테이블(표) 형태로 필수 간호 중재 목록 출력
    st.write("**📋 필수 간호 중재 목록**")
    df = pd.DataFrame(table_data)
    st.table(df)
