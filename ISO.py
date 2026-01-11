import pycountry

codes = [c.alpha_2.lower() for c in pycountry.countries]
print(codes)