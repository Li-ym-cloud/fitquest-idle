import sqlite3
import os
from .models.player import PlayerStatus

DB_PATH = "game_data.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY,
            name TEXT, level INTEGER, xp INTEGER, xp_next INTEGER,
            points INTEGER, physical_atk INTEGER, magic_atk INTEGER,
            max_hp INTEGER, current_hp INTEGER, death_count INTEGER
        )
    ''')
    cursor.execute("SELECT count(*) FROM player")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO player (id, name, level, xp, xp_next, points, physical_atk, magic_atk, max_hp, current_hp, death_count)
            VALUES (1, 'Hero', 1, 0, 10, 0, 5, 2, 100, 100, 0)
        ''')
    conn.commit()
    conn.close()

def load_player():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        data = dict(row)
        # 打印日志观察读取结果
        print(f"--- DB LOAD: XP={data['xp']}, Level={data['level']} ---")
        return PlayerStatus(**data)
    return PlayerStatus()

def save_player(p: PlayerStatus):
    print(f"[数据库日志] 正在写入 SQLite. XP 目标值: {p.xp}")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 严格核对字段顺序：level(1), xp(2), xp_next(3), points(4), physical_atk(5), magic_atk(6), max_hp(7), current_hp(8), death_count(9)
        cursor.execute('''
            UPDATE player SET 
            level=?, xp=?, xp_next=?, points=?, physical_atk=?, 
            magic_atk=?, max_hp=?, current_hp=?, death_count=?
            WHERE id = 1
        ''', (p.level, p.xp, p.xp_next, p.points, p.physical_atk, 
              p.magic_atk, p.max_hp, p.current_hp, p.death_count))
        conn.commit()
        print("[数据库日志] SQLite UPDATE 成功完成")
    except Exception as e:
        print(f"[数据库日志] SQLite 写入失败: {e}")
    finally:
        conn.close()