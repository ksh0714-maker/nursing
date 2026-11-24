def check_vital(symptom, temp):
    risk_score = 40  # 기본 정상 위험도 점수
    
    # 1) 체온(temp) 자체의 정상/비정상 범위를 먼저 판단
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

    # 2) 선택한 주요 증상에 따른 추가 위험도 및 안내 문구 조합
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
