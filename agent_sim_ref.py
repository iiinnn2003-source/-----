import random
import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np
from pathlib import Path

# Настройка логгинга для корпоративных систем
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Agent:
    cog_ability: float
    is_alpha: bool = False

def simulate_step(
    agents: List[Agent], 
    has_alpha: bool, 
    rng: random.Random,
    config: Dict
) -> List[Agent]:
    
    next_gen = []
    alpha_agent: Optional[Agent] = None
    
    if has_alpha and agents:
        # Поиск лидера среди выживших (O(N))
        alpha_agent = max(agents, key=lambda x: x.cog_ability)

    cogs = np.array([a.cog_ability for a in agents])
    
    # Векторизованный расчет стоимости ресурсов (быстрее циклов)
    brain_costs = cogs * config["brain_cost_factor"]
    resource_penalties = np.maximum(0, brain_costs - (config["resource_level"] * 2.0))
    
    # Вместо: pair_bonus_mask = rng.random(len(agents)) < 0.7
    pair_bonus_mask = [rng.random() < 0.7 for _ in agents]
    pair_bonus = np.where(pair_bonus_mask, 0.3, 0.0)

    avg_offspring_list = []
    current_cogs = []

    for i, agent in enumerate(agents):
        base_offspring = 1.5
        
        if has_alpha and alpha_agent is not None:
            if agent == alpha_agent:
                avg_offspring = 4.0
                current_cog = agent.cog_ability
            elif rng.random() < 0.3:  # Близость к альфе
                avg_offspring = 2.5
                # Штраф за делегирование когнитивной нагрузки
                current_cog = agent.cog_ability * (1 - config["beta_cog_reduction"])
            else:
                avg_offspring = 1.0 - (0.3 - pair_bonus[i])
                current_cog = agent.cog_ability
        else:
            avg_offspring = base_offspring + cogs[i] - (0.3 - pair_bonus[i])
            current_cog = agent.cog_ability

        avg_offspring -= resource_penalties[i]
        avg_offspring = max(0.1, avg_offspring)
        
        avg_offspring_list.append(avg_offspring)
        current_cogs.append(current_cog)

    # Генерация потомков
    for i, agent in enumerate(agents):
        actual_offspring = max(0, int(rng.gauss(avg_offspring_list[i], 0.5)))
        for _ in range(actual_offspring):
            mutation = rng.gauss(0, 0.1)
            child_cog = max(0.1, current_cogs[i] + mutation)
            next_gen.append(Agent(child_cog))
            
    return next_gen

def run_simulation(generations: int = 20, start_pop: int = 50, seed: int = 42, output_dir: str = "outputs") -> Dict:
    logger.info(f"Запуск симуляции: {generations} поколений, N={start_pop}")
    
    history = {"avg_cog": [], "mode": []}
    population = [Agent(cog_ability=1.0) for _ in range(start_pop)]
    
    # Единый генератор случайных чисел для детерминизма
    rng = random.Random(seed)
    
    # Гиперпараметры вынесены отдельно
    config = {
        "brain_cost_factor": 1.5,
        "beta_cog_reduction": 0.1,
        "resource_level": 1.0
    }

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    for gen in range(1, generations + 1):
        mode = "Эгалитаризм" if gen <= generations // 2 else "Иерархия"
        
        # Логируем ключевые метрики каждые 5 шагов
        if gen % 5 == 0 or gen == 1:
            current_avg = sum(a.cog_ability for a in population) / len(population)
            logger.info(f"[Gen {gen}/{generations}] Mode: {mode}, Avg Cog: {current_avg:.3f}")

        population = simulate_step(population, has_alpha=(gen > generations // 2), rng=rng, config=config)
        
        if not population:
            logger.error("Популяция вымерла!")
            break
            
        avg_cog = sum(a.cog_ability for a in population) / len(population)
        history["avg_cog"].append(avg_cog)
        history["mode"].append(mode)
        
    # Сохранение результатов строго в папку outputs
    file_path = output_path / "simulation_log.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
        
    logger.info(f"Симуляция завершена. Данные сохранены в {file_path.resolve()}")
    return history

if __name__ == "__main__":
    results = run_simulation(generations=20, start_pop=50)
