# Item 6: Prefer Multiple Assignment Unpacking Over Indexing

favorite_volcanoes = {
    'Kilauea': 'shield volcano',
    'Mt Helens': 'stratovolcano',
    'Mt Pelee': 'stratovolcano',
}

for name, category in favorite_volcanoes.items():
    print(f'{name} is a {category}')