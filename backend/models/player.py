from pydantic import BaseModel
import time

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
    death_count: int = 0  # 建议初始为0

    def reset_to_initial(self):
        """
        重置玩家到1级初始状态
        """
        self.level = 1
        self.xp = 0
        self.xp_next = 10
        self.points = 0
        
        # 恢复初始战斗属性
        self.physical_atk = 1
        self.magic_atk = 1
        self.max_hp = 100
        self.current_hp = 100
        
        # 时间戳更新为当前，防止跨度计算错误
        self.last_update = time.time()
        
        # 死亡计数是否重置取决于你的设计需求
        # self.death_count = 0 
        
        return self