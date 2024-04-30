
def validate_city(city):
    validated_cities = [
        {'Bucuresti': ['bucharest', 'bucuresti']},
        {'Cluj-Napoca': ['cluj napoca', 'cluj']},
        {'Bolintin-Deal': ['bolintin-deal', 'bolintin - deal']},
        {'Campulung': ['campulung muscel', 'campulung Muscel']},
        {'Poiana Lacului': ['poiana lacului']},
        {'Dragomiresti Vale': ['com.  dragomiresti vale']}

    ]

    for item in validated_cities:
        for key, value in item.items():
            if city.lower() in value:
                return key
    return city



