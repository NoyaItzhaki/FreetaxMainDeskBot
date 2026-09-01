def extract(amount: float, include_vat: bool = False, vat_rate: float = 18.0) -> dict:
    """
    מחשבון מע"מ גמיש לפייתון.
    
    :param amount: הסכום לחישוב (ברוטו או נטו)
    :param include_vat: True אם הסכום כבר כולל מע"מ (לחילוץ), False אם הסכום ללא מע"מ (להוספה)
    :param vat_rate: אחוז המע"מ (ברירת מחדל 18%)
    :return: דיקשנרי עם כל נתוני החישוב (נטו, ברוטו וסכום המע"מ)
    """
    rate_factor = 1 + (vat_rate / 100)
    
    if include_vat:
        # חילוץ מע"מ מסכום כולל
        gross = round(amount, 2)
        net = round(gross / rate_factor, 2)
        vat_amount = round(gross - net, 2)
    else:
        # הוספת מע"מ לסכום נטו
        net = round(amount, 2)
        gross = round(net * rate_factor, 2)
        vat_amount = round(gross - net, 2)
        
    return {
        "net": net,
        "vat_amount": vat_amount,
        "gross": gross,
        "vat_rate": f"{vat_rate}%"
    }
