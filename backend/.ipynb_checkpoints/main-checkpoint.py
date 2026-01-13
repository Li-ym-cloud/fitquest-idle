import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.player import PlayerStatus, FitnessData
# from .core.engine import GameEngine  # 如果逻辑移到了 main，暂时可以不引用

app = FastAPI(title="FitQuest Idle API")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟数据库：初始化一个具有 RPG 属性的玩家
db_player = PlayerStatus(
    name="Hero", 
    last_update=time.time(),
    physical_atk=1,
    magic_atk=1,
    points=3
)

@app.post("/level-up")
async def level_up():
    """触发升级逻辑：当经验满时，前端调用此接口"""
    global db_player
    
    db_player.level += 1
    db_player.points += 1       # 核心：升级给 1 点
    db_player.xp = 0            # 重置当前经验
    db_player.xp_next *= 2      # 经验需求翻倍
    
    print(f"玩家升级到 {db_player.level}, 获得 1 点, 下级需要 {db_player.xp_next}")
    return db_player

@app.get("/game-status")
async def get_status():
    """前端刷新或进入页面时调用，获取当前存档"""
    global db_player
    return db_player

@app.post("/sync-fitness")
async def sync_fitness(data: dict):
    """
    接收健身数据：
    1. 计算额外属性点
    2. 返回给前端即时更新
    """
    global db_player
    steps = data.get("steps", 0)
    # 逻辑：每 5000 步给 1 个点数
    extra_points = steps // 5000
    
    if extra_points > 0:
        db_player.points += extra_points
        return {
            "message": f"同步成功！获得 {extra_points} 点数", 
            "points": db_player.points,
            "current_atk": db_player.physical_atk # 保持兼容性
        }
    return {"message": "步数不足，继续努力！", "points": db_player.points}

@app.post("/upgrade")
async def upgrade_stat(stat_type: str):
    """加点接口：由前端点击 +1 按钮触发"""
    global db_player
    if db_player.points <= 0:
        raise HTTPException(status_code=400, detail="没有足够的属性点")
    
    if stat_type == "physical":
        db_player.physical_atk += 1
    elif stat_type == "magic":
        db_player.magic_atk += 1
    elif stat_type == "hp":
        db_player.max_hp += 50
        db_player.current_hp = db_player.max_hp
    else:
        raise HTTPException(status_code=400, detail="未知属性类型")
    
    db_player.points -= 1
    return db_player  # 返回修改后的完整玩家对象，方便前端直接覆盖状态

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)