import random
from pydantic import BaseModel

class Monster(BaseModel):
    name: str
    level: int
    hp: int
    max_hp: int
    physical_atk: int
    magic_atk: int

    @classmethod
    def create_random(cls, player_level: int):
        """
        根据玩家等级动态生成一只怪
        实现 90% 较弱，10% 较强的分布逻辑
        """
        prefixes_weak = ["虚弱的", "瘦小的", "迷茫的", "普通的"]
        prefixes_strong = ["狂暴的", "远古", "钢铁", "受诅咒的"]
        names = ["史莱姆", "哥布林", "骷髅兵", "傀儡", "地狱犬"]
        
        # 1. 基础属性线 (以此为基准进行缩放)
        hp_base = 40 + (player_level * 15)
        atk_base = 3 + (player_level * 1.8)
        
        # 2. 判定稀有度 (0-1 随机数)
        rarity_roll = random.random()
        
        if rarity_roll > 0.9:
            # --- 强力怪 (10% 概率) ---
            multiplier = random.uniform(1.2, 1.6) # 1.2倍到1.6倍强度
            name_prefix = random.choice(prefixes_strong)
            # 精英怪可能会有额外的魔法伤害加成
            m_atk = int(atk_base * 0.5) 
        else:
            # --- 普通/弱怪 (90% 概率) ---
            multiplier = random.uniform(0.6, 0.9) # 只有基础属性的 60% 到 90%
            name_prefix = random.choice(prefixes_weak)
            m_atk = 0

        # 3. 计算最终属性
        final_hp = int(hp_base * multiplier)
        final_p_atk = int(atk_base * multiplier)
        
        # 4. 组装名字
        full_name = f"{name_prefix}{random.choice(names)}"

        return cls(
            name=full_name,
            level=player_level,
            hp=final_hp,
            max_hp=final_hp,
            physical_atk=final_p_atk,
            magic_atk=m_atk
        )