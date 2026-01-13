import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.monster import Monster
from .database import init_db, load_player, save_player

# --- 1. 日志配置 ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GameServer")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. 初始化数据 ---
init_db()
db_player = load_player()
db_monster = Monster.create_random(db_player.level)

logger.info(f"游戏服务启动。玩家: {db_player.name}, 当前等级: {db_player.level}, XP: {db_player.xp}")

# --- 3. 辅助函数 ---
def apply_dynamic_nerf(monster, death_count, player_level):
    multiplier = max(0.5, 1.0 - (death_count * 0.01))
    monster.max_hp = int(monster.max_hp * multiplier)
    monster.hp = monster.max_hp
    monster.physical_atk = max(1, int(monster.physical_atk * multiplier))
    return monster

# --- 4. 路由接口 ---
@app.get("/game-status")
async def get_status():
    global db_monster,db_player
    if db_monster.hp <= 0:
        db_monster = apply_dynamic_nerf(
            Monster.create_random(db_player.level), 
            db_player.death_count, 
            db_player.level
        )
    return {"player": db_player, "monster": db_monster}

@app.post("/add-xp")
async def add_xp(amount: int = 2):
    global db_player
    logger.info(f"[XP增加前] 内存XP: {db_player.xp}")
    
    db_player.xp += amount
    db_player.current_hp = db_player.max_hp # 击杀回血
    
    save_player(db_player) # 写入数据库
    logger.info(f"[XP增加后] 内存XP: {db_player.xp} (已同步数据库)")
    
    return db_player

@app.post("/upgrade")
async def upgrade(stat_type: str):
    global db_player
    if db_player.points <= 0:
        raise HTTPException(status_code=400, detail="点数不足")
    
    if stat_type == "physical":
        db_player.physical_atk += 1
    elif stat_type == "magic":
        db_player.magic_atk += 1
    elif stat_type == "hp":
        db_player.max_hp += 20
        db_player.current_hp = db_player.max_hp
    
    db_player.points -= 1
    save_player(db_player) # 写入 SQLite
    return db_player

@app.post("/respawn")
async def respawn():
    global db_player, db_monster
    # 追踪 XP 是否在这里丢失
    logger.info(f"[复活开始] 接口被触发。当前内存 XP: {db_player.xp}, 死亡次数: {db_player.death_count}")
    
    db_player.death_count += 1
    db_player.current_hp = db_player.max_hp
    
    # 执行持久化
    save_player(db_player)
    
    # 刷新怪
    db_monster = apply_dynamic_nerf(
        Monster.create_random(db_player.level), 
        db_player.death_count, 
        db_player.level
    )
    
    logger.info(f"[复活结束] 数据已保存。返回 XP: {db_player.xp}, 死亡次数: {db_player.death_count}")
    return {"player": db_player, "monster": db_monster}

@app.post("/level-up")
async def level_up():
    global db_player
    logger.info(f"[升级开始] 当前等级: {db_player.level}")
    
    db_player.level += 1
    db_player.xp = 0 # 只有这里会重置 XP
    db_player.xp_next = int(db_player.xp_next * 1.6)
    db_player.death_count = 0 
    db_player.points += 1
    db_player.current_hp = db_player.max_hp
    
    save_player(db_player)
    logger.info(f"[升级结束] 新等级: {db_player.level}, XP已清零并存档")
    
    monster = Monster.create_random(db_player.level)
    return {"player": db_player, "monster": monster}

@app.post("/upgrade")
async def upgrade(stat_type: str):
    if db_player.points <= 0:
        raise HTTPException(status_code=400, detail="点数不足")
    
    if stat_type == "physical": db_player.physical_atk += 1
    elif stat_type == "magic": db_player.magic_atk += 1
    elif stat_type == "hp": 
        db_player.max_hp += 20
        db_player.current_hp = db_player.max_hp
    
    db_player.points -= 1
    save_player(db_player)
    logger.info(f"[属性提升] 类型: {stat_type}, 剩余点数: {db_player.points}")
    return db_player

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)