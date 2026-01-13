import random
from pydantic import BaseModel

class Monster(BaseModel):
    name: str
    level: int
    hp: int
    max_hp: int
    physical_atk: int
    magic_atk: int

    @staticmethod
    def create_random(player_level: int):
        """根据玩家等级动态生成一只怪"""
        names = ["暗影潜行者", "熔岩史莱姆", "远古傀儡", "虚空之眼"]
        
        # 属性平衡逻辑：等级越高，属性波动越大
        hp_base = 40 + (player_level * 15)
        atk_base = 2 + (player_level * 1.5)
        
        # 随机分配物理和魔法倾向
        is_magic_type = random.random() > 0.5
        
        p_atk = random.randint(1, int(atk_base))
        m_atk = random.randint(1, int(atk_base))
        
        if is_magic_type:
            m_atk += player_level
            name = f"魔导·{random.choice(names)}"
        else:
            p_atk += player_level
            name = f"狂暴·{random.choice(names)}"

        hp_final = random.randint(hp_base, hp_base + 30)

        return Monster(
            name=name,
            level=player_level,
            hp=hp_final,
            max_hp=hp_final,
            physical_atk=p_atk,
            magic_atk=m_atk
        )

    @classmethod
    def create_random(cls, player_level):
        prefixes = ["狂暴的", "虚弱的", "远古", "阴险的", "钢铁", "受诅咒的"]
        names = ["史莱姆", "哥布林", "骷髅兵", "傀儡", "地狱犬"]
        
        name = random.choice(prefixes) + random.choice(names)
        
        # 基础属性根据玩家等级提升
        base_hp = 40 + (player_level * 15)
        base_atk = 3 + (player_level * 2)
        
        return cls(
            name=name,
            level=player_level,
            hp=base_hp,
            max_hp=base_hp,
            physical_atk=base_atk,
            magic_atk=0
        )