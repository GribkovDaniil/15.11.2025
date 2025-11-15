import random
import math

class GeneticAlgorithm:
    def __init__(self):
        self.population_size = 0
        self.generations = 0
        self.crossover_prob = 0.0
        self.mutation_prob = 0.0
        self.chromosome_length = 0
        self.x_min = 0
        self.x_max = 0
        
    def get_user_input(self):
        """Получение параметров от пользователя"""
        print("=== Генетический алгоритм для максимизации функции f(x) = -(x-5)² + 25 ===")
        
        self.population_size = int(input("Размер популяции (рекомендуется 20): ") or "20")
        self.generations = int(input("Количество поколений (рекомендуется 50): ") or "50")
        self.crossover_prob = float(input("Вероятность кроссовера (рекомендуется 0.8): ") or "0.8")
        self.mutation_prob = float(input("Вероятность мутации (рекомендуется 0.1): ") or "0.1")
        
        # Диапазон x
        self.x_min = float(input("Минимальное значение x (рекомендуется 0): ") or "0")
        self.x_max = float(input("Максимальное значение x (рекомендуется 10): ") or "10")
        
        # Определяем длину хромосомы на основе требуемой точности
        precision = 0.01  # Точность до 0.01
        self.chromosome_length = math.ceil(math.log2((self.x_max - self.x_min) / precision))
        
        print(f"\nПараметры алгоритма:")
        print(f"- Размер популяции: {self.population_size}")
        print(f"- Количество поколений: {self.generations}")
        print(f"- Вероятность кроссовера: {self.crossover_prob}")
        print(f"- Вероятность мутации: {self.mutation_prob}")
        print(f"- Длина хромосомы: {self.chromosome_length} бит")
        print(f"- Диапазон x: [{self.x_min}, {self.x_max}]")
        print()
    
    def fitness_function(self, x):
        """Функция приспособленности: f(x) = -(x-5)² + 25"""
        return -(x - 5) ** 2 + 25
    
    def binary_to_decimal(self, binary_string):
        """Преобразование двоичной строки в десятичное число"""
        decimal = int(binary_string, 2)
        # Масштабируем к диапазону [x_min, x_max]
        x = self.x_min + decimal * (self.x_max - self.x_min) / (2 ** self.chromosome_length - 1)
        return x
    
    def decimal_to_binary(self, decimal):
        """Преобразование десятичного числа в двоичную строку (не используется в инициализации)"""
        # Масштабируем decimal к [0, 2^chromosome_length-1]
        scaled = int((decimal - self.x_min) * (2 ** self.chromosome_length - 1) / (self.x_max - self.x_min))
        binary_string = format(scaled, f'0{self.chromosome_length}b')
        return binary_string
    
    def create_individual(self):
        """Создание случайной особи (двоичная строка)"""
        individual = ''.join(random.choice('01') for _ in range(self.chromosome_length))
        return individual
    
    def initialize_population(self):
        """Инициализация начальной популяции"""
        population = [self.create_individual() for _ in range(self.population_size)]
        return population
    
    def evaluate_population(self, population):
        """Оценка приспособленности популяции"""
        fitness_scores = []
        for individual in population:
            x = self.binary_to_decimal(individual)
            fitness = self.fitness_function(x)
            fitness_scores.append(fitness)
        return fitness_scores
    
    def selection(self, population, fitness_scores):
        """Турнирная селекция"""
        selected = []
        tournament_size = 3
        
        for _ in range(self.population_size):
            # Выбираем случайных особей для турнира
            tournament_indices = random.sample(range(len(population)), tournament_size)
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]
            
            # Выбираем победителя турнира (с наибольшей приспособленностью)
            winner_index = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
            selected.append(population[winner_index])
        
        return selected
    
    def crossover(self, parent1, parent2):
        """Одноточечный кроссовер"""
        if random.random() < self.crossover_prob:
            # Выбираем случайную точку кроссовера
            crossover_point = random.randint(1, self.chromosome_length - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            return child1, child2
        else:
            # Если кроссовер не происходит, возвращаем родителей
            return parent1, parent2
    
    def mutation(self, individual):
        """Точечная мутация"""
        mutated = list(individual)
        for i in range(len(mutated)):
            if random.random() < self.mutation_prob:
                # Инвертируем бит
                mutated[i] = '0' if mutated[i] == '1' else '1'
        return ''.join(mutated)
    
    def run(self):
        """Запуск генетического алгоритма"""
        # Получаем параметры от пользователя
        self.get_user_input()
        
        # Инициализация популяции
        population = self.initialize_population()
        best_individual = None
        best_fitness = -float('inf')
        
        print("Запуск генетического алгоритма...")
        print("Поколение | Лучшая приспособленность | Лучший x")
        print("-" * 50)
        
        # Основной цикл алгоритма
        for generation in range(self.generations):
            # Оценка приспособленности
            fitness_scores = self.evaluate_population(population)
            
            # Обновление лучшего решения
            current_best_fitness = max(fitness_scores)
            current_best_index = fitness_scores.index(current_best_fitness)
            current_best_individual = population[current_best_index]
            
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best_individual
            
            # Вывод информации о текущем поколении
            best_x = self.binary_to_decimal(current_best_individual)
            print(f"{generation+1:9} | {current_best_fitness:23.6f} | {best_x:8.4f}")
            
            # Селекция
            selected = self.selection(population, fitness_scores)
            
            # Кроссовер и мутация
            new_population = []
            
            for i in range(0, self.population_size, 2):
                parent1 = selected[i]
                parent2 = selected[(i + 1) % self.population_size]  # Циклический выбор
                
                child1, child2 = self.crossover(parent1, parent2)
                
                child1 = self.mutation(child1)
                child2 = self.mutation(child2)
                
                new_population.extend([child1, child2])
            
            # Обновление популяции
            population = new_population[:self.population_size]
        
        # Вывод результатов
        best_x = self.binary_to_decimal(best_individual)
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ:")
        print(f"Лучшее решение: x = {best_x:.6f}")
        print(f"Лучшая приспособленность: {best_fitness:.6f}")
        print(f"Двоичное представление: {best_individual}")
        print(f"Ожидаемый максимум: x = 5.0, f(x) = 25.0")
        
        return best_individual, best_fitness

# Запуск программы
if __name__ == "__main__":
    ga = GeneticAlgorithm()
    ga.run()
