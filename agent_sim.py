
import random

class Agent:
    def __init__(self, cog_ability, is_alpha=False):
        self.cog_ability = cog_ability  # когнитивные способности (аналог "размера мозга")
        self.is_alpha = is_alpha
        self.offspring_count = 0

def simulate_generation(agents, has_alpha, alpha_agent=None, resource_level=1.0, beta_cog_reduction=0.1):
    """
    has_alpha: bool - есть ли в группе формальный лидер
    alpha_agent: Agent - объект альфы, если есть
    resource_level: общий уровень ресурсов в среде (1.0 = норма, 0.5 = дефицит)
    """
    
    next_gen_agents = []

   
    for agent in agents:

        # Базовая плодовитость
        base_offspring = 1.5

        # Стоимость мозга: чем выше когнитивные способности, тем больше нужно ресурсов
        brain_cost = agent.cog_ability * 1.5  # коэффициент стоимости
        # Если ресурсов мало, а мозг большой — агент рискует не выжить или оставить меньше детей
        resource_penalty = max(0, brain_cost - (resource_level * 2.0))
        # Чем сильнее дефицит ресурсов, тем выше штраф


        has_stable_pair = random.random() < 0.7  # условная вероятность наличия устойчивой связи
        if has_stable_pair:
            pair_bonus = 0.3  # небольшой бонус к приспособленности за стабильность
        else:
            pair_bonus = 0

        
        if has_alpha and alpha_agent is not None:
            # РЕЖИМ С АЛЬФОЙ: приспособленность зависит от близости к альфе
            # Для простоты: если агент — альфа, он получает макс. потомство.
            # Если агент близок к альфе (рандомно считаем близость), он тоже получает бонус.
            if agent == alpha_agent:
                avg_offspring = 4.0  # максимум у альфы
            elif random.random() < 0.3:  # условная "близость" к альфе у 30% группы
                avg_offspring = 2.5
                agent.cog_ability = agent.cog_ability * (1 - beta_cog_reduction)
            else:
                avg_offspring = 1.0 - (0.3 - pair_bonus)     # В иерархической группе бонус от пары почти не работает — важнее близость к альфе
        else:
            # РЕЖИМ БЕЗ АЛЬФЫ: приспособленность прямо пропорциональна когнитивным способностям
            # Базовая плодовитость + бонус за когнитивные способности + бонус за стабильную пару
            avg_offspring = base_offspring + (agent.cog_ability * 1.0) - (0.3 - pair_bonus)
            
        # Применяем штраф из-за дефицита ресурсов
        avg_offspring -= resource_penalty       
        # Не даём упасть ниже нуля
        avg_offspring = max(0.1, avg_offspring)

        # Реальное число потомков (с небольшим шумом)
        actual_offspring = max(0, int(random.gauss(avg_offspring, 0.5)))
        agent.offspring_count = actual_offspring
        
        # Создаем потомков с небольшой мутацией когнитивных способностей
        for _ in range(actual_offspring):
            mutation = random.gauss(0, 0.1)
            child_cog = max(0.1, agent.cog_ability + mutation)
            next_gen_agents.append(Agent(child_cog))
            
    return next_gen_agents

# --- Запуск симуляции ---
# Начальное состояние: группа без альфы, средние когнитивные способности 1.0
population = [Agent(cog_ability=1.0) for _ in range(20)]

print("Поколение | Средний 'размер мозга' (cog_ability) | Режим ")
for gen in range(1, 21):
    # Первые 10 поколений - без альфы (рост мозга)
    if gen <= 10:
        population = simulate_generation(population, has_alpha=False)
        mode = "Без альфы"
    else:
        # После 10-го поколения появляется альфа (смена режима)
        alpha = population[0]
        alpha.is_alpha = True
        population = simulate_generation(population, has_alpha=True, alpha_agent=alpha)
        mode = "С альфой и бетами"

    
    avg_cog = sum(a.cog_ability for a in population) / len(population) if population else 0
    print(f"{gen:9} | {avg_cog:.2f} | {mode} ")



# print ("Сценарий острова Флорес: постоянный дефицит ресурсов")
# print("Поколение | Средний cog_ability | Ресурсы | Режим")
# population = [Agent(cog_ability=1.0) for _ in range(20)]  # изначально чуть умнее

# for gen in range(1, 21):
#     # Всегда низкий уровень ресурсов (дефицит)
#     population = simulate_generation(population, has_alpha=False, resource_level=0.5)
#     avg_cog = sum(a.cog_ability for a in population) / len(population) if population else 0
#     print(f"{gen:9} | {avg_cog:.2f} | 0.5 (дефицит) | Без альфы")

