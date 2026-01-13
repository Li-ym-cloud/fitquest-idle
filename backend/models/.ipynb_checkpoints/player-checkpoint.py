from pydantic import BaseModel

class FitnessData(BaseModel):
    steps: int = 0
    punch_count: int = 0

class PlayerStatus(BaseModel):
    name: str = "Hero"
    level: int = 1
    xp: int = 0
    xp_next: int = 10  # 升级所需经验
    points: int = 0    # 剩余属性点
    
    # 战斗属性
    physical_atk: int = 1
    magic_atk: int = 1
    max_hp: int = 100
    current_hp: int = 100
    
    last_update: float = 0.0
    death_count:int = 1