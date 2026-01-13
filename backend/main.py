from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json, os, time
from .models.player import PlayerStatus
from .models.monster import Monster

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

DATA_FILE = "player_data.json"

def save_db():
    data = db_player.dict()
    data['death_count'] = getattr(db_player, 'death_count', 0)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_db():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                p = PlayerStatus(**data)
                p.death_count = data.get('death_count', 0)
                return p
        except: pass
    p = PlayerStatus(name="Hero", last_update=time.time())
    p.death_count = 0
    return p

db_player = load_db()
db_monster = Monster.create_random(db_player.level)

def apply_linear_nerf(monster, death_count):
    # 核心逻辑：死亡1次下调1%，2次下调2%
    multiplier = max(0.5, 1.0 - (death_count * 0.01))
    monster.max_hp = int(monster.max_hp * multiplier)
    monster.hp = monster.max_hp
    monster.physical_atk = max(1, int(monster.physical_atk * multiplier))
    return monster

@app.get("/game-status")
async def get_status():
    global db_monster
    if db_monster.hp <= 0:
        db_monster = apply_linear_nerf(Monster.create_random(db_player.level), db_player.death_count)
    return {"player": db_player, "monster": db_monster, "death_count": db_player.death_count}

@app.post("/respawn")
async def respawn():
    global db_player, db_monster
    db_player.death_count += 1
    db_player.current_hp = db_player.max_hp
    db_monster = apply_linear_nerf(Monster.create_random(db_player.level), db_player.death_count)
    save_db()
    return {"player": db_player, "monster": db_monster}

@app.post("/level-up")
async def level_up():
    db_player.level += 1
    db_player.points += 1
    db_player.xp = 0
    db_player.xp_next = int(db_player.xp_next * 1.6)
    global db_monster
    db_monster = apply_linear_nerf(Monster.create_random(db_player.level), db_player.death_count)
    save_db()
    return {"player": db_player, "monster": db_monster}

@app.post("/upgrade")
async def upgrade(stat_type: str):
    if db_player.points <= 0: raise HTTPException(400, "点数不足")
    if stat_type == "physical": db_player.physical_atk += 1
    elif stat_type == "magic": db_player.magic_atk += 1
    elif stat_type == "hp": 
        db_player.max_hp += 20
        db_player.current_hp = db_player.max_hp
    db_player.points -= 1
    save_db()
    return db_player

if __name__ == "__main__":
    import uvicorn
    # 启动 8000 端口
    uvicorn.run(app, host="0.0.0.0", port=8000)