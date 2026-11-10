# Item 7: Prefer enumerate() Over range()

hazard_list = ['landslide', 'volcanic eruption', 'GLOF', 'glacier detachment']

print("\nUsing enumerate():")
for i, hazard in enumerate(hazard_list, 1):
    print(f'{i}: {hazard}')