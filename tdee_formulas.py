def calculate_lbm(gender, weight, height):
    """
    Calculates the Lean Body Mass based on the Boer formula
    """
    if gender.lower() == 'f':
        lbm = 0.252 * weight + 0.473 * height - 48.3
    else:
        lbm = 0.407 * weight + 0.267 * height - 19.2
    
    return lbm


def calculate_bmr(lbm):
    """
    Calculates a person BMR(Basal Metabolic Rate).
    It takes the LBM, multiplies it by 21.6
    and then adds 370 to it.
    """
    bmr = lbm * 21.6 + 370

    return bmr


def calculate_tef(bmr):
    """
    Calculates the Thermic Effect of Food.
    It multiplies the BMR by 0.1
    """
    tef = bmr * 0.1
    
    return tef


def calculate_tea(bmr, activity_level):
    """
    Calculates the Thermic Effect of Activity.
    It first translates the activity level 
    to a specific activity factor.
    Then it multiplies this last one for the BMR
    """
    activity_factor = ""

    if activity_level == "SED":
        activity_factor = 1.2
    elif activity_level == "LA":
        activity_factor = 1.375
    elif activity_level == "MA":
        activity_factor = 1.55
    elif activity_level == "VA":
        activity_factor = 1.725
    else:
        activity_factor = 1.9
    
    tea = (bmr * activity_factor) - bmr

    return tea


def calculate_tdee(gender, weight, height, activity_level):
    """
    Calculates the Total Daily Energy Expenditure:
    it sums up the bmr, tea and tef.
    """
    lbm = calculate_lbm(gender, weight, height)
    bmr = calculate_bmr(lbm)
    tef = calculate_tef(bmr)
    tea = calculate_tea(bmr, activity_level)

    tdee = round(bmr + tea + tef)

    return tdee
