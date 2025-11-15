Вариант 11. Генетический алгоритм для оптимизации


Алгоритм работы генетического алгоритма
1. Инициализация и ввод параметров
Код: self.get_user_input()

2. Создание начальной популяции
Код: population = self.initialize_population()

3. Основной цикл по поколениям
Код: for generation in range(self.generations):

4. Оценка и селекция
Код: fitness_scores = self.evaluate_population(population) и selected = self.selection(population, fitness_scores)

5. Генетические операторы (кроссовер и мутация)
Код: child1, child2 = self.crossover(parent1, parent2) и child1 = self.mutation(child1)

6. Формирование новой популяции и вывод результатов
Код: population = new_population[:self.population_size] и финальный вывод результатов



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






=== Генетический алгоритм для максимизации функции f(x) = -(x-5)² + 25 ===
Размер популяции (рекомендуется 20): 20
Количество поколений (рекомендуется 50): 50
Вероятность кроссовера (рекомендуется 0.8): 0.8
Вероятность мутации (рекомендуется 0.1): 0.1
Минимальное значение x (рекомендуется 0): 0
Максимальное значение x (рекомендуется 10): 10

Параметры алгоритма:
- Размер популяции: 20
- Количество поколений: 50
- Вероятность кроссовера: 0.8
- Вероятность мутации: 0.1
- Длина хромосомы: 10 бит
- Диапазон x: [0.0, 10.0]

Запуск генетического алгоритма...
Поколение | Лучшая приспособленность | Лучший x
--------------------------------------------------
        1 |               24.967297 |   4.8192
        2 |               24.994625 |   5.0733
        3 |               24.999785 |   5.0147
        4 |               24.999785 |   5.0147
        5 |               24.998829 |   5.0342
        6 |               24.998829 |   5.0342
        7 |               24.998829 |   5.0342
        8 |               24.999403 |   5.0244
        9 |               24.998829 |   5.0342
       10 |               24.999403 |   5.0244
       11 |               24.999785 |   5.0147
       12 |               24.999785 |   5.0147
       13 |               24.999403 |   5.0244
       14 |               24.999403 |   5.0244
       15 |               24.999976 |   5.0049
       16 |               24.999785 |   5.0147
       17 |               24.999785 |   5.0147
       18 |               24.999403 |   5.0244
       19 |               24.999403 |   5.0244
       20 |               24.999403 |   5.0244
       21 |               24.999403 |   5.0244
       22 |               24.999403 |   5.0244
       23 |               24.999403 |   5.0244
       24 |               24.999403 |   5.0244
       25 |               24.999403 |   5.0244
       26 |               24.999976 |   5.0049
       27 |               24.999976 |   5.0049
       28 |               24.999976 |   5.0049
       29 |               24.999976 |   5.0049
       30 |               24.999976 |   5.0049
       31 |               24.999976 |   5.0049
       32 |               24.999976 |   5.0049
       33 |               24.999976 |   5.0049
       34 |               24.999976 |   5.0049
       35 |               24.999976 |   5.0049
       36 |               24.999976 |   5.0049
       37 |               24.999976 |   5.0049
       38 |               24.999976 |   5.0049
       39 |               24.999976 |   5.0049
       40 |               24.999976 |   5.0049
       41 |               24.999976 |   5.0049
       42 |               24.999976 |   5.0049
       43 |               24.999976 |   5.0049
       44 |               24.999976 |   5.0049
       45 |               24.999976 |   5.0049
       46 |               24.999976 |   5.0049
       47 |               24.999976 |   5.0049
       48 |               24.998829 |   5.0342
       49 |               24.999785 |   5.0147
       50 |               24.999976 |   5.0049

==================================================
РЕЗУЛЬТАТЫ:
Лучшее решение: x = 5.004888
Лучшая приспособленность: 24.999976
Двоичное представление: 1000000000
Ожидаемый максимум: x = 5.0, f(x) = 25.0


O(G × N × L)
Где:

G - количество поколений (константа ≈ 50)

N - размер популяции (константа ≈ 20)

L - длина хромосомы (зависит от точности, обычно 10-20 бит)
Временная сложность алгоритма составляет O(G × N × L), где G - количество поколений, N - размер популяции, L - длина хромосомы. Эта сложность возникает потому, что для каждого из G поколений мы обрабатываем N особей, выполняя для каждой операции с L битами (оценка приспособленности, кроссовер, мутация). Основные затраты приходятся на преобразование двоичных строк в числа и генетические операции, которые линейно зависят от длины хромосомы.

На практике алгоритм работает за константное время O(1), поскольку все параметры G, N, L фиксированы и не зависят от размера входных данных. При типичных значениях G=50, N=20, L=20 общее количество операций составляет около 20,000, что является постоянной величиной для данного алгоритма.



Вывод: Алгоритм имеет линейную сложность относительно произведения своих параметров, но поскольку параметры фиксированы - на практике работает за константное время.

11. Имитация отжига

Имитация отжига — это метаэвристический алгоритм, вдохновленный физическим процессом отжига металлов, где материал нагревается и медленно охлаждается для достижения состояния с минимальной энергией. В оптимизации алгоритм используется для поиска глобального оптимума, позволяя на ранних этапам принимать "худшие" решения, чтобы избежать застревания в локальных оптимумах.

Роль параметра температуры критична: высокая начальная температура позволяет алгоритму активно принимать решения, ухудшающие текущее состояние (исследование пространства решений). По мере снижения температуры алгоритм постепенно переходит к фазе эксплуатации, все чаще принимая только улучшающие решения и стабилизируясь near-оптимальном решении. Температура thus управляет балансом между исследованием и эксплуатацией.
