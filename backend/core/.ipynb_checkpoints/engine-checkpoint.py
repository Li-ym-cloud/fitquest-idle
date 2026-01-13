from ..models.player import PlayerStatus, FitnessData

class GameEngine:
    @staticmethod
    def calculate_bonus(data: FitnessData):
        """
        核心算法：将健身数据转化为游戏数值加成
        $$Character\_Power = (Steps \times 0.01) + (Punch\_Count \times 0.5)$$
        """
        atk_bonus = (data.steps * 0.01) + (data.punch_count * 0.5)
        return atk_bonus

    @staticmethod
    def process_tick(player: PlayerStatus, current_time: float):
        """计算挂机收益"""
        delta_time = current_time - player.last_update
        if delta_time <= 0:
            return player

        # 挂机公式：每秒收益 = 攻击力 * 0.1
        income = player.atk * delta_time * 0.1
        player.gold += income
        player.last_update = current_time
        return player