import math
import numpy as np
import matplotlib.pyplot as plt

class DropCalculator:
    def __init__(self):
        self.aircraft_trajectory = None
        self.drop_location = None
        self.desired_distance = 10.0
        self.flight_azimuth = 0.0
        
    def calculate_drop_point(self, aircraft_trajectory, drop_location, 
                           flight_azimuth, desired_distance=10.0):
        """
        Рассчитывает оптимальную точку сброса на траектории самолета
        
        Args:
            aircraft_trajectory: список точек траектории самолета [(x1,y1), (x2,y2), ...]
            drop_location: целевая точка приземления (x,y)
            flight_azimuth: азимутальный угол траектории полета в градусах
            desired_distance: желаемое расстояние сброса (перпендикуляр к траектории)
            
        Returns:
            optimal_point: оптимальная точка сброса на траектории (x,y)
            actual_distance: фактическое расстояние до цели
            along_track_distance: расстояние вдоль траектории от ближайшей точки
        """
        self.aircraft_trajectory = aircraft_trajectory
        self.drop_location = drop_location
        self.desired_distance = desired_distance
        self.flight_azimuth = flight_azimuth
        
        # Конвертируем угол в радианы
        azimuth_rad = math.radians(flight_azimuth)
        
        # Находим ближайшую точку на траектории к целевой локации
        closest_point, min_distance, closest_idx = self._find_closest_point()
        
        if closest_point is None:
            return None, None, None
        
        # Рассчитываем вектор перпендикуляра к траектории
        perpendicular_vector = self._calculate_perpendicular_vector(azimuth_rad)
        
        # Вычисляем смещение от цели по перпендикуляру
        perpendicular_offset = self._calculate_perpendicular_offset(closest_point, perpendicular_vector)
        
        # Определяем направление смещения вдоль траектории
        along_track_distance = self._calculate_along_track_distance(
            perpendicular_offset, desired_distance, azimuth_rad
        )
        
        # Находим точку сброса на траектории
        drop_point = self._find_point_on_trajectory(closest_idx, along_track_distance, azimuth_rad)
        
        # Проверяем расстояние до цели
        actual_distance = math.sqrt((drop_point[0] - drop_location[0])**2 + 
                                  (drop_point[1] - drop_location[1])**2)
        
        return drop_point, actual_distance, along_track_distance
    
    def _find_closest_point(self):
        """Находит ближайшую точку на траектории к целевой локации и ее индекс"""
        min_distance = float('inf')
        closest_point = None
        closest_idx = -1
        
        for i, point in enumerate(self.aircraft_trajectory):
            distance = math.sqrt((point[0] - self.drop_location[0])**2 + 
                               (point[1] - self.drop_location[1])**2)
            if distance < min_distance:
                min_distance = distance
                closest_point = point
                closest_idx = i
                
        return closest_point, min_distance, closest_idx
    
    def _calculate_perpendicular_vector(self, azimuth_rad):
        """Вычисляет вектор перпендикулярный направлению полета"""
        # Направляющий вектор траектории
        direction_vector = (math.cos(azimuth_rad), math.sin(azimuth_rad))
        
        # Перпендикулярный вектор (поворот на 90 градусов)
        perpendicular_vector = (-direction_vector[1], direction_vector[0])
        
        return perpendicular_vector
    
    def _calculate_perpendicular_offset(self, closest_point, perpendicular_vector):
        """Вычисляет смещение цели от траектории по перпендикуляру"""
        # Вектор от ближайшей точки к цели
        vector_to_target = (self.drop_location[0] - closest_point[0],
                          self.drop_location[1] - closest_point[1])
        
        # Проекция на перпендикулярное направление (скалярное произведение)
        perpendicular_offset = (vector_to_target[0] * perpendicular_vector[0] + 
                              vector_to_target[1] * perpendicular_vector[1])
        
        return perpendicular_offset
    
    def _calculate_along_track_distance(self, perpendicular_offset, desired_distance, azimuth_rad):
        """Вычисляет расстояние вдоль траектории для достижения желаемого перпендикулярного расстояния"""
        # Разница между фактическим и желаемым перпендикулярным расстоянием
        offset_difference = perpendicular_offset - desired_distance
        
        # Для компенсации этой разницы нужно двигаться вдоль траектории
        # Используем тангенс угла (геометрическая зависимость)
        along_track_distance = offset_difference / math.tan(math.radians(45))  # Упрощенная модель
        
        return along_track_distance
    
    def _find_point_on_trajectory(self, start_idx, distance, azimuth_rad):
        """Находит точку на траектории на заданном расстоянии от стартовой точки"""
        if start_idx < 0 or start_idx >= len(self.aircraft_trajectory):
            return self.aircraft_trajectory[0] if self.aircraft_trajectory else None
        
        start_point = self.aircraft_trajectory[start_idx]
        
        # Направляющий вектор траектории
        direction_vector = (math.cos(azimuth_rad), math.sin(azimuth_rad))
        
        # Вычисляем новую точку
        new_point = (start_point[0] + direction_vector[0] * distance,
                   start_point[1] + direction_vector[1] * distance)
        
        return new_point
    
    def visualize(self, drop_point, actual_distance, along_track_distance):
        """Визуализирует результаты расчета"""
        if not self.aircraft_trajectory or not self.drop_location:
            return
        
        plt.figure(figsize=(12, 10))
        
        # Траектория самолета
        x_traj = [p[0] for p in self.aircraft_trajectory]
        y_traj = [p[1] for p in self.aircraft_trajectory]
        plt.plot(x_traj, y_traj, 'b-', label='Траектория самолета', linewidth=3)
        plt.plot(x_traj, y_traj, 'bo', markersize=6, alpha=0.7)
        
        # Целевая локация
        plt.plot(self.drop_location[0], self.drop_location[1], 'ro', 
                markersize=12, label='Цель приземления', markeredgewidth=2, markeredgecolor='black')
        
        # Точка сброса
        if drop_point:
            plt.plot(drop_point[0], drop_point[1], 'go', 
                    markersize=10, label='Точка сброса', markeredgewidth=2, markeredgecolor='black')
            
            # Линия сброса
            plt.plot([drop_point[0], self.drop_location[0]], 
                    [drop_point[1], self.drop_location[1]], 
                    'r--', linewidth=2, label=f'Траектория падения: {actual_distance:.2f} ед.')
            
            # Перпендикуляр от траектории к цели
            closest_point, _, _ = self._find_closest_point()
            if closest_point:
                plt.plot([closest_point[0], self.drop_location[0]], 
                        [closest_point[1], self.drop_location[1]], 
                        'm:', linewidth=1, label='Перпендикуляр к траектории')
        
        plt.xlabel('X координата', fontsize=12)
        plt.ylabel('Y координата', fontsize=12)
        plt.title('Расчет точки сброса с самолета\n(точка сброса всегда на траектории)', fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        
        # Добавляем информацию о расстояниях
        if drop_point and along_track_distance is not None:
            plt.text(0.02, 0.98, 
                    f'Желаемое расстояние: {self.desired_distance} ед.\n'
                    f'Фактическое расстояние: {actual_distance:.2f} ед.\n'
                    f'Смещение вдоль траектории: {along_track_distance:.2f} ед.',
                    transform=plt.gca().transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                    fontsize=10)
        
        plt.tight_layout()
        plt.show()

# Пример использования
def main():
    # Создаем калькулятор
    calculator = DropCalculator()
    
    # Задаем параметры
    aircraft_trajectory = [(0, 0), (10, 5), (20, 10), (30, 15), (40, 20)]
    drop_location = (25, 5)
    flight_azimuth = 26.565  # градусов (примерно arctan(5/10))
    desired_distance = 10.0
    
    # Выполняем расчет
    drop_point, actual_distance, along_track_distance = calculator.calculate_drop_point(
        aircraft_trajectory, drop_location, flight_azimuth, desired_distance
    )
    
    # Выводим результаты
    if drop_point:
        print("=" * 50)
        print("РЕЗУЛЬТАТЫ РАСЧЕТА ТОЧКИ СБРОСА")
        print("=" * 50)
        print(f"Траектория самолета: {aircraft_trajectory}")
        print(f"Целевая локация: {drop_location}")
        print(f"Азимут полета: {flight_azimuth}°")
        print(f"Желаемое расстояние: {desired_distance} единиц")
        print("-" * 50)
        print(f"Оптимальная точка сброса: ({drop_point[0]:.2f}, {drop_point[1]:.2f})")
        print(f"Фактическое расстояние до цели: {actual_distance:.2f} единиц")
        print(f"Смещение вдоль траектории: {along_track_distance:.2f} единиц")
        print(f"Отклонение от желаемого: {abs(actual_distance - desired_distance):.2f} единиц")
        print("=" * 50)
        
        # Визуализируем
        calculator.visualize(drop_point, actual_distance, along_track_distance)
    else:
        print("Не удалось рассчитать точку сброса")

if __name__ == "__main__":
    main()