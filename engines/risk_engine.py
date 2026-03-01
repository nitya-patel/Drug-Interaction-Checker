def calculate_risk(conflicts, age_warnings, gender_warnings):
    """
    Calculates numerical risk score and returns a risk level.
    Severity weights:
    Mild -> 1
    Moderate -> 2
    Severe -> 3
    Contraindicated -> 5
    
    Each warning adds 3 points.
    Max score is capped at 100.
    """
    weights = {
        "Mild": 1,
        "Moderate": 2,
        "Severe": 3,
        "Contraindicated": 5
    }
    
    score = 0
    
    for conflict in conflicts:
        severity = conflict.get("severity", "Mild")
        score += weights.get(severity, 1) * 10
        
    score += len(age_warnings) * 15
    score += len(gender_warnings) * 20
    
    # Cap between 0 and 100
    risk_score = max(0, min(100, score))
    
    if risk_score > 50:
        risk_level = "High"
    elif risk_score > 20:
        risk_level = "Moderate"
    else:
        risk_level = "Low"
        
    return risk_score, risk_level
