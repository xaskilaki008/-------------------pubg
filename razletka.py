import math

def calculate_hypotenuse_from_squares():
    """
    Расчет гипотенузы по количеству квадратов в игре
    """
    print("=" * 50)
    print("РАСЧЕТ ГИПОТЕНУЗЫ ПО КВАДРАТАМ ИГРЫ")
    print("=" * 50)
    
    # Ввод данных
    try:
        squares_right = int(input("Количество квадратов вправо: "))
        squares_down = int(input("Количество квадратов вниз: "))
        
        # Размеры квадратов (по вашим данным)
        square_size_diagonal = 144  # м по диагонали 45°
        square_size_straight = 100  # м прямо (вверх/вниз/влево/вправо)
        
        print("\nВыберите тип расчета:")
        print("1 - По диагонали (144м на квадрат)")
        print("2 - По прямым направлениям (100м на квадрат)")
        
        choice = input("Ваш выбор (1 или 2): ")
        
        if choice == "1":
            # Расчет через диагональные расстояния
            distance_right = squares_right * square_size_diagonal
            distance_down = squares_down * square_size_diagonal
            
            # Гипотенуза от двух катетов
            hypotenuse = math.sqrt(distance_right**2 + distance_down**2)
            
            print(f"\nРасчет по диагонали 45° (144м/квадрат):")
            print(f"Расстояние вправо: {squares_right} кв. × 144м = {distance_right} м")
            print(f"Расстояние вниз: {squares_down} кв. × 144м = {distance_down} м")
            
        elif choice == "2":
            # Расчет через прямые расстояния
            distance_right = squares_right * square_size_straight
            distance_down = squares_down * square_size_straight
            
            # Гипотенуза от двух катетов
            hypotenuse = math.sqrt(distance_right**2 + distance_down**2)
            
            print(f"\nРасчет по прямым направлениям (100м/квадрат):")
            print(f"Расстояние вправо: {squares_right} кв. × 100м = {distance_right} м")
            print(f"Расстояние вниз: {squares_down} кв. × 100м = {distance_down} м")
        else:
            print("Неверный выбор!")
            return
            
        # Угол к горизонту
        angle = math.degrees(math.atan2(distance_down, distance_right))
        
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ РАСЧЕТА:")
        print("=" * 50)
        print(f"Квадратов вправо: {squares_right}")
        print(f"Квадратов вниз: {squares_down}")
        print(f"Гипотенуза: {hypotenuse:.2f} м")
        print(f"Угол к горизонту: {angle:.1f}°")
        print("=" * 50)
        
        # Дополнительная информация
        print(f"\nДОПОЛНИТЕЛЬНО:")
        print(f"В километрах: {hypotenuse/1000:.2f} км")
        print(f"Для игры (округленно): {round(hypotenuse)} м")
        
    except ValueError:
        print("Ошибка! Вводите только целые числа для квадратов.")

# Автоматический расчет для примера
def quick_calculation(squares_right, squares_down, use_diagonal=True):
    """
    Быстрый расчет для заданных значений
    """
    if use_diagonal:
        square_size = 144
        method = "диагональ"
    else:
        square_size = 100  
        method = "прямо"
    
    distance_right = squares_right * square_size
    distance_down = squares_down * square_size
    hypotenuse = math.sqrt(distance_right**2 + distance_down**2)
    angle = math.degrees(math.atan2(distance_down, distance_right))
    
    print(f"\nБыстрый расчет ({method}):")
    print(f"{squares_right}кв вправо + {squares_down}кв вниз")
    print(f"Гипотенуза: {hypotenuse:.0f} м, Угол: {angle:.1f}°")
    return hypotenuse

# Запуск основной программы
calculate_hypotenuse_from_squares()

# Примеры быстрых расчетов
print("\n" + "="*50)
print("ПРИМЕРЫ РАСЧЕТОВ:")
print("="*50)

# Пример 1: 5 квадратов вправо, 3 вниз
quick_calculation(5, 3, use_diagonal=True)
quick_calculation(5, 3, use_diagonal=False)

print("\n" + "="*50)

# Пример 2: 10 квадратов вправо, 2 вниз  
quick_calculation(10, 2, use_diagonal=True)
quick_calculation(10, 2, use_diagonal=False)