def __scale(val, src, dst):
    """
    :param val: value
    :param src: source range, e.g. 0 - 100
    :param dst: destination range, e.g. 555 - 888
    :return: val corrected to be proportional to the destination range
    """
    return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


source_scales = {
    'oil_temp': (266, 393),
    'water_temp': (266, 393),
    'oil_pressure': (0, 551)
}


print("OIL-TEMP: \n\tHIGH: " + str(int(__scale(369, source_scales['oil_temp'], (0, 290)))) + "\n\tLOW: " + str(int(__scale(344, source_scales['oil_temp'], (0, 290)))))
print("WATER-TEMP: \n\tHIGH: " + str(int(__scale(377, source_scales['water_temp'], (0, 290)))) + "\n\tLOW: " + str(int(__scale(344, source_scales['water_temp'], (0, 290)))))
print("OIL-PRESSURE: \n\tHIGH: " + str(int(__scale(377, source_scales['oil_pressure'], (0, 290)))) + "\n\tLOW: " + str(int(__scale(206, source_scales['oil_pressure'], (0, 290)))))

