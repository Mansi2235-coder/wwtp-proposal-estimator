def pollutant_load(flow, concentration):
    return flow * concentration / 1000


def removed_load(flow, bod_in, bod_out):
    return flow * (bod_in - bod_out) / 1000


def sludge_production(flow, bod_in, bod_out, yield_y, decay_kd, srt):
    y_obs = yield_y / (1 + decay_kd * srt)
    return y_obs * removed_load(flow, bod_in, bod_out)


def tank_volume(flow, bod_in, bod_out, yield_y, decay_kd, srt, mlvss):
    sludge = sludge_production(flow, bod_in, bod_out, yield_y, decay_kd, srt)
    return srt * sludge * 1000 / mlvss


def oxygen_demand(flow, bod_in, bod_out, yield_y, decay_kd, srt, bod_ratio):
    ultimate_bod = removed_load(flow, bod_in, bod_out) / bod_ratio
    sludge = sludge_production(flow, bod_in, bod_out, yield_y, decay_kd, srt)
    return ultimate_bod - 1.42 * sludge


def hrt(volume, flow):
    return volume / flow * 24


def fm_ratio(flow, bod_in, volume, mlvss):
    return flow * bod_in / (volume * mlvss)


def check_fm(fm):
    if fm < 0.2:
        return "F/M is too low"
    elif fm > 0.4:
        return "F/M is too high"
    else:
        return "F/M is OK"

if __name__ == "__main__":
    # Inputs
    flow = 10000
    bod_in = 250
    bod_out = 20
    yield_y = 0.6
    decay_kd = 0.08
    srt = 10
    mlvss = 2500
    bod_ratio = 0.68

    # Calculations
    volume = tank_volume(flow, bod_in, bod_out, yield_y, decay_kd, srt, mlvss)
    fm = fm_ratio(flow, bod_in, volume, mlvss)

    # Report
    print("Influent load (kg/day):", pollutant_load(flow, bod_in))
    print("Removed load (kg/day):", removed_load(flow, bod_in, bod_out))
    print("Sludge (kg VSS/day):", round(sludge_production(flow, bod_in, bod_out, yield_y, decay_kd, srt), 1))
    print("Tank volume (m3):", round(volume, 1))
    print("HRT (hours):", round(hrt(volume, flow), 1))
    print("F/M ratio:", round(fm, 2))
    print(check_fm(fm))
    print("Oxygen demand (kg O2/day):", round(oxygen_demand(flow, bod_in, bod_out, yield_y, decay_kd, srt, bod_ratio), 1))