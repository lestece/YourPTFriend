def lbm(gender, weight, height):
    """
    Calculates the Lean Body Mass based on the Boer formula
    """
    if gender.lower() == 'f':
        lbm = 0.252 * weight + 0.473 * height - 48.3
    else:
        lbm = 0.407 * weight + 0.267 * height - 19.2
    
    return lbm


def bmr(lbm):
    """
    Calculates a person BMR(Basal Metabolic Rate).
    It takes the LBM, multiplies it by 21.6
    and then adds 370 to it.
    """
    bmr = lbm * 21.6 + 370
