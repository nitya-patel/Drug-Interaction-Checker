def validate_patient(patient_data, drugs, drugs_db):
    """
    Validates patient data against drug restrictions.
    Returns lists of age warnings and gender warnings.
    """
    age_warnings = []
    gender_warnings = []
    
    patient_age = patient_data.get('age')
    patient_gender = patient_data.get('gender')
    
    # Create lookup dict for faster access
    drug_info_map = {d['name'].lower(): d for d in drugs_db}
    
    for drug in drugs:
        drug_lower = drug.lower()
        if drug_lower in drug_info_map:
            info = drug_info_map[drug_lower]
            drug_name = info['name']
            
            # Age check
            if patient_age is not None:
                if patient_age < info.get('min_age', 0) or patient_age > info.get('max_age', 200):
                    age_warnings.append(f"{drug_name} is typically not recommended for age {patient_age}. (Valid range: {info.get('min_age')}-{info.get('max_age')})")
            
            # Gender check
            restriction = info.get('gender_restriction', 'None')
            if restriction != 'None' and patient_gender is not None:
                if patient_gender.lower() != restriction.lower():
                    gender_warnings.append(f"{drug_name} is restricted to {restriction} patients.")
                    
    return age_warnings, gender_warnings
