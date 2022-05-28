d_l = {
    "speed": 5,
    # %battery charge in idle mode %/min
    "battery_charge": 10,
    # %battery loss per time delivery and returning %/s
    "battery_loss": 1.5,
    # time loading medication
    "loading": 60
}
d_m = {
    # speed en m/s
    "speed": 5,
    # %battery charge in idle mode %/min
    "battery_charge": 9,
    # %battery loss per distance %/km
    "battery_loss": 1.2,
    # time loading medication
    "loading": 60
}
d_c = {
    # speed en m/s
    "speed": 5,
    # %battery charge in idle mode %/min
    "battery_charge": 8,
    # %battery loss per distance %/km
    "battery_loss": 1.1,
    # time loading medication
    "loading": 60
}
d_h = {
    # speed en m/s
    "speed": 5,
    # %battery charge in idle mode %/min
    "battery_charge": 7,
    # %battery loss per distance %/km
    "battery_loss": 1,
    # time loading medication
    "loading": 60
}
stats_dm = {
    "Lightweight": d_l,
    "Middleweight": d_m,
    "Cruiserweight": d_c,
    "Heavyweight": d_h,
}