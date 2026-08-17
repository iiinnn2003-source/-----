import random
import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class Agent:
    cog_ability: float
    is_alpha: bool = False

def simulate_step(agents: List[Agent], has_alpha: bool, resource_level: float = 1.0, 
                  brain_cost_factor: float = 1.5, beta_cog_reduction: float = 0.1) -> List[Agent]:
    
    next_gen = []
    alpha_agent = None
    
    # Находим текущего лидера (если режим иерархии)
    if has_alpha and agents:
        # Альфой становится самый когнитивно способный индивид прошлого поколения
        alpha_agent = max(agents, key=lambda x: x.cog_ability)

    for agent in agents:
        base_offspring = 1.5
        
        # Стоимость поддержания мозга
        brain_cost = agent.cog_ability * brain_cost_factor
        resource_penalty = max(0, brain_cost - (resource_level * 2.0))
        
        # Бонус за пару (стабильность связей)
        pair_bonus = 0.3 if random.random() < 0.7 else 0.0

        # РАСЧЕТ ПРИСПОСОБЛЕННОСТИ (Суть вашей модели)
        if has_alpha and alpha_agent is not None:
            if agent == alpha_agent:
                avg_offspring = 4.0
                current_cog = agent.cog_ability
            elif random.random() < 0.3: # Близость к альфе (Беты)
                avg_offspring = 2.5
                # СТРУКТУРНОЕ СНИЖЕНИЕ: бета-агенты снижают затраты на мозг
                current_cog = agent.cog_ability * (1 - beta_cog_reduction)
            else:
                avg_offspring = 1.0 - (0.3 - pair_bonus)
                current_cog = agent.cog_ability
        else:
            # Эгалитарный режим: выживает умнейший
            avg_offspring = base_offspring + (agent.cog_ability * 1.0) - (0.3 - pair_bonus)
            current_cog = agent.cog_ability

        avg_offspring -= resource_penalty
        avg_offspring = max(0.1, avg_offspring)
        
        actual_offspring = max(0, int(random.gauss(avg_offspring, 0.5)))
        
        for _ in range(actual_offspring):
            mutation = random.gauss(0, 0.1)
            child_cog = max(0.1, current_cog + mutation)
            next_gen.append(Agent(child_cog))
            
    return next_gen

# --- ИНСТРУМЕНТАРИЙ ДЛЯ ПИТЧА ---
def run_simulation(generations: int = 20, start_pop: int = 50) -> Dict:
    history = {"avg_cog": [], "mode": []}
    population = [Agent(cog_ability=1.0) for _ in range(start_pop)]

    for gen in range(1, generations + 1):
        # Точка перегиба ровно посередине для наглядности графиков
        mode = "Без альфы" if gen <= generations // 2 else "С альфой"
        
        population = simulate_step(population, has_alpha=(gen > generations // 2))
        
        if population:
            avg_cog = sum(a.cog_ability for a in population) / len(population)
        else:
            avg_cog = 0
            
        history["avg_cog"].append(avg_cog)
        history["mode"].append(mode)
        
    return history

if __name__ == "__main__":
    results = run_simulation()
    
    # Демонстрация цифр для письма (Поколения 14, 15, 16, 17)
    print("Динамика среднего 'размера мозга' при смене парадигмы:")
    idx = len(results["avg_cog"])
    print(f"T-{idx-2} (Эгалитаризм): {results['avg_cog'][-3]:.2f}")
    print(f"T-{idx-1} (Перед сменой): {results['avg_cog'][-2]:.2f}")
    print(f"T-{idx}   (Появление Альфы): {results['avg_cog'][-1]:.2f}")
    
    # Выгрузка для построения графика аналитиками Сбера
    with open('simulation_log.json', 'w') as f:
        json.dump(results, f, indent=2)
        
