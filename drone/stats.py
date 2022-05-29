d_l = {
    "speed": 10,
    # %battery charge in idle mode %/min
    "battery_charge": 0.08,
    # %battery loss per time delivery and returning %/s
    "battery_loss": 0.0115,
    # time loading medication
    "loading": 60
}
d_m = {
    # speed en m/s
    "speed": 10,
    # %battery charge in idle mode %/s
    "battery_charge": 0.07,
    # %battery loss per distance %/s
    "battery_loss": 0.012,
    # time loading medication
    "loading": 60
}
d_c = {
    # speed en m/s
    "speed": 10,
    # %battery charge in idle mode %/min
    "battery_charge": 0.06,
    # %battery loss per distance %/km
    "battery_loss": 0.0125,
    # time loading medication
    "loading": 60
}
d_h = {
    # speed en m/s
    "speed": 10,
    # %battery charge in idle mode %/min
    "battery_charge": 0.05,
    # %battery loss per distance %/s
    "battery_loss": 0.013,
    # time loading medication
    "loading": 60
}
stats_dm = {
    "Lightweight": d_l,
    "Middleweight": d_m,
    "Cruiserweight": d_c,
    "Heavyweight": d_h,
}
