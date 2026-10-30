# analysis.py

# This function checks whether a value is LOW, NORMAL or HIGH
def check_range(value, low, high):

    if value < low:
        return "LOW"

    elif value > high:
        return "HIGH"

    else:
        return "NORMAL"


# Main blood report analysis function
def analyze_report(data):

    results = []

    # Get patient's gender
    gender = data["gender"].lower()

    # =====================================================
    # 1. WBC - White Blood Cells
    # =====================================================

    wbc = float(data["wbc"])

    if wbc < 4000:
        status = "LOW"
        concern = "Low WBC count. This may be associated with some infections, medicines, or immune-related conditions."

    elif wbc > 10000:
        status = "HIGH"
        concern = "High WBC count. This may be associated with infection, inflammation, or other conditions."

    else:
        status = "NORMAL"
        concern = "WBC count is within the reference range."

    results.append({
        "name": "White Blood Cells (WBC)",
        "value": wbc,
        "unit": "cells/µL",
        "range": "4,000 - 10,000",
        "status": status,
        "concern": concern
    })


    # =====================================================
    # 2. Hemoglobin
    # =====================================================

    hemoglobin = float(data["hemoglobin"])

    if gender == "male":

        low = 13.2
        high = 16.6
        normal_range = "13.2 - 16.6 g/dL"

    else:

        low = 11.6
        high = 15.0
        normal_range = "11.6 - 15.0 g/dL"


    if hemoglobin < low:

        status = "LOW"
        concern = "Low hemoglobin. Anemia may be possible and further evaluation may be needed."

    elif hemoglobin > high:

        status = "HIGH"
        concern = "High hemoglobin. Dehydration or other conditions may be associated."

    else:

        status = "NORMAL"
        concern = "Hemoglobin is within the reference range."


    results.append({
        "name": "Hemoglobin (Hb)",
        "value": hemoglobin,
        "unit": "g/dL",
        "range": normal_range,
        "status": status,
        "concern": concern
    })


    # =====================================================
    # 3. RBC - Red Blood Cells
    # =====================================================

    rbc = float(data["rbc"])

    if gender == "male":

        low = 4.35
        high = 5.65
        normal_range = "4.35 - 5.65 million/µL"

    else:

        low = 3.92
        high = 5.13
        normal_range = "3.92 - 5.13 million/µL"


    if rbc < low:

        status = "LOW"
        concern = "Low RBC count. This may be associated with anemia or blood-loss-related conditions."

    elif rbc > high:

        status = "HIGH"
        concern = "High RBC count. Dehydration or increased red blood cell production may be associated."

    else:

        status = "NORMAL"
        concern = "RBC count is within the reference range."


    results.append({
        "name": "Red Blood Cells (RBC)",
        "value": rbc,
        "unit": "million/µL",
        "range": normal_range,
        "status": status,
        "concern": concern
    })


    # =====================================================
    # 4. Platelets
    # =====================================================

    platelets = float(data["platelets"])

    if gender == "male":

        low = 135000
        high = 317000
        normal_range = "135,000 - 317,000 /µL"

    else:

        low = 157000
        high = 371000
        normal_range = "157,000 - 371,000 /µL"


    if platelets < low:

        status = "LOW"
        concern = "Low platelet count. This is called thrombocytopenia and may increase bleeding risk."

    elif platelets > high:

        status = "HIGH"
        concern = "High platelet count. This is called thrombocytosis and may be associated with inflammation or other conditions."

    else:

        status = "NORMAL"
        concern = "Platelet count is within the reference range."


    results.append({
        "name": "Platelet Count",
        "value": int(platelets),
        "unit": "/µL",
        "range": normal_range,
        "status": status,
        "concern": concern
    })


    # =====================================================
    # 5. Fasting Blood Glucose
    # =====================================================

    glucose = float(data["glucose"])


    if glucose < 70:

        status = "LOW"
        concern = "Low blood glucose. This may indicate hypoglycemia, especially if symptoms are present."

    elif glucose <= 99:

        status = "NORMAL"
        concern = "Fasting blood glucose is within the normal reference range."

    else:

        status = "HIGH"
        concern = "Elevated fasting glucose. Prediabetes or diabetes may be a concern and should be evaluated with appropriate medical testing."


    results.append({
        "name": "Fasting Blood Glucose",
        "value": glucose,
        "unit": "mg/dL",
        "range": "70 - 99 mg/dL",
        "status": status,
        "concern": concern
    })


    # =====================================================
    # 6. Total Cholesterol
    # =====================================================

    cholesterol = float(data["cholesterol"])


    if cholesterol < 200:

        status = "NORMAL"
        concern = "Total cholesterol is in the desirable range."

    else:

        status = "HIGH"
        concern = "Elevated total cholesterol may be associated with increased cardiovascular risk."


    results.append({
        "name": "Total Cholesterol",
        "value": cholesterol,
        "unit": "mg/dL",
        "range": "< 200 mg/dL",
        "status": status,
        "concern": concern
    })


    # =====================================================
    # 7. Creatinine
    # =====================================================

    creatinine = float(data["creatinine"])


    if gender == "male":

        low = 0.7
        high = 1.3
        normal_range = "0.7 - 1.3 mg/dL"

    else:

        low = 0.5
        high = 0.95
        normal_range = "0.5 - 0.95 mg/dL"


    if creatinine < low:

        status = "LOW"
        concern = "Low creatinine can occur for several reasons, including lower muscle mass."

    elif creatinine > high:

        status = "HIGH"
        concern = "High creatinine may indicate reduced kidney function, but creatinine alone cannot diagnose kidney disease."

    else:

        status = "NORMAL"
        concern = "Creatinine is within the reference range."


    results.append({
        "name": "Creatinine",
        "value": creatinine,
        "unit": "mg/dL",
        "range": normal_range,
        "status": status,
        "concern": concern
    })


    # =====================================================
    # SUMMARY
    # =====================================================

    total = len(results)

    normal = 0
    low = 0
    high = 0


    for result in results:

        if result["status"] == "NORMAL":

            normal = normal + 1

        elif result["status"] == "LOW":

            low = low + 1

        elif result["status"] == "HIGH":

            high = high + 1


    summary = {
        "total": total,
        "normal": normal,
        "low": low,
        "high": high
    }


    # =====================================================
    # OVERALL REPORT MESSAGE
    # =====================================================

    if high == 0 and low == 0:

        overall_message = "All tested parameters are within the reference ranges used by this system."

    elif high > 0 and low > 0:

        overall_message = "Some parameters are outside the reference ranges. Please review the individual results and consult a healthcare professional."

    elif high > 0:

        overall_message = "Some parameters are higher than the reference ranges. Further medical evaluation may be appropriate."

    else:

        overall_message = "Some parameters are lower than the reference ranges. Further medical evaluation may be appropriate."


    return results, summary, overall_message