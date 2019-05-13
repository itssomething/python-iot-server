def f(x):
    return {
        'Clear': 1,
        'Clouds': 2,
        'Drizzle': 3,
        'Mist': 4,
        'Thunderstorm': 5
    }[x]

print(f('Thunderstorm'))