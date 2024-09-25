
def validate_city(city):
    validated_cities = [
        {'Bucuresti': ['bucharest', 'bucuresti','romania', 'negotiable', 'ilfov', '€150', '~156','€3','€44','budget']},
        {'Cluj-Napoca': ['cluj napoca', 'cluj']},
        {'Bolintin-Deal': ['bolintin-deal', 'bolintin - deal']},
        {'Campulung': ['campulung muscel', 'campulung Muscel']},
        {'Poiana Lacului': ['poiana lacului']},
        {'Dragomiresti Vale': ['com.  dragomiresti vale']},
        {'Targu-Mures': ['targu mures']},
        {'Piatra-Neamt': ['neamt', 'neamţ','piatra neamţ']},
        {'Miercurea Ciuc': ['harghita']},
        {'Craiova': ['dolj']},
        {'Alba Iulia': ['iulia']},
        {'Targu Jiu': ['jiu']},
        {'Ramnicu Valcea': ['valcea']},
        {'Satu Mare': ['mare']},
        {'Slobozia': ['ialomita', 'ialomița']},
        {'Oradea': ['bihor']}

    ]

    if isinstance(city, str):
        for item in validated_cities:
            for key, value in item.items():
                if city.lower() in value:
                    return key
    elif isinstance(city, list):
        res = city
        for item in validated_cities:
            for key, value in item.items():
                for city_item in city:
                    if city_item.lower() in value:
                        res.remove(city_item)
                        res.append(key)
        return res
    return city


print(validate_city(['Iasi', 'Cluj']))
print(validate_city('Bucuresti'))
