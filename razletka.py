import math

# Просто введите эти значения
AZIMUTH = 16    # градусов
HYPOTENUSE = 100  # метров

# Расчет
distance = HYPOTENUSE * math.cos(math.radians(AZIMUTH))
height = HYPOTENUSE * math.sin(math.radians(AZIMUTH))

print(f"При азимуте {AZIMUTH}° и гипотенузе {HYPOTENUSE} м:")
print(f"Расстояние по горизонтали: {distance:.2f} м")
print(f"Высота: {height:.2f} м")