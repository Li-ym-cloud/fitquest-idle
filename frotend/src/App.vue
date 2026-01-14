<template>
  <div class="game-root">
    <div class="game-container">
      
      <div class="battle-section">
        <BattleArena />
      </div>

      <div class="main-content">
        
        <div class="left-side">
          <StatPanel />
          
          <div class="xp-mini-card">
            <div class="xp-info">
              <span>经验值 (EXP)</span>
              <span>{{ gameState.player.xp }} / {{ gameState.player.xp_next }}</span>
            </div>
            <div class="xp-bar-bg">
              <div class="xp-bar-fill" :style="{ width: (gameState.player.xp / gameState.player.xp_next * 100) + '%' }"></div>
            </div>
          </div>

          <button @click="showModal = true" class="sync-button">
            ⌚ 同步健身步数
          </button>

          <div class="danger-zone">
            <button @click="handleReset" class="reset-button">
              🧨 删档重置进度
            </button>
          </div>
        </div>

        <div class="right-side">
          <div class="log-panel">
            <div class="log-header">
              <div class="header-left">
                <span class="dot"></span> 实时战斗记录
              </div>
              <span class="death-count">死亡削弱: -{{ gameState.player.death_count || 0 }}%</span>
            </div>
            <div class="log-body">
              <transition-group name="list">
                <div v-for="(log, i) in gameState.logs" :key="log.id" 
                     class="log-row" :class="log.type"
                     :style="{ opacity: 1 - (i * 0.15) }">
                  <span class="time">[{{ log.time }}]</span>
                  <span class="text">{{ log.msg }}</span>
                </div>
              </transition-group>
            </div>
          </div>
        </div>
      </div>

    </div>

    <SyncModal v-if="showModal" @close="showModal = false" />
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue';
import { gameState, actions } from './store/game';
import StatPanel from './components/StatPanel.vue';
import BattleArena from './components/BattleArena.vue';
import SyncModal from './components/SyncModal.vue';

const showModal = ref(false);

/**
 * 核心战斗循环
 * 使用 setInterval 驱动，每 1.6秒 进行一轮攻防
 */
function startBattleLoop() {
  console.log("战斗系统：启动循环...");
  
  setInterval(async () => {
    // 判定条件：玩家未死、敌人存在且有血量、非重置锁定状态
    if (gameState.isDead) return;
    if (!gameState.enemy || gameState.enemy.hp <= 0 || gameState.enemy.name === "寻找中...") {
      return;
    }

    // --- 1. 玩家攻击逻辑 ---
    gameState.isAttacking = true;
    const pDmg = gameState.player.physical_atk + gameState.player.magic_atk;
    gameState.enemy.hp -= pDmg;
    actions.addLog(`⚔️ 你发动攻击，造成了 ${pDmg} 点伤害`, 'info');

    // --- 2. 怪物反击 (延迟 400ms 以配合动画感) ---
    setTimeout(() => {
      gameState.isAttacking = false;
      if (gameState.enemy.hp > 0 && !gameState.isDead) {
        const mDmg = gameState.enemy.physical_atk;
        gameState.player.current_hp -= mDmg;
        actions.addLog(`💥 [${gameState.enemy.name}] 反击，你失去了 ${mDmg} 生命`, 'danger');
        
        if (gameState.player.current_hp <= 0) {
          triggerDeath();
        }
      }
    }, 400);

    // --- 3. 检查怪物死亡结算 ---
    if (gameState.enemy.hp <= 0) {
      gameState.enemy.hp = 0; 
      await actions.handleMonsterDefeat(); 
    }
  }, 1600); 
}

/**
 * 统一死亡处理逻辑
 */
async function triggerDeath() {
  if (gameState.isDead) return;
  gameState.isDead = true;
  gameState.player.current_hp = 0;
  
  actions.addLog(`❌ 战败！正在复活...`, "system");

  try {
    const res = await axios.post('/respawn'); 
    // 死亡惩罚展示时间：5秒
    setTimeout(() => {
      gameState.player = res.data.player;
      gameState.enemy = res.data.monster;
      gameState.isDead = false;
      actions.addLog(`🛡️ 复活成功，已为您削弱怪物。`, 'success');
    }, 5000);
  } catch (e) {
    console.error("复活请求失败:", e);
    gameState.isDead = false; // 失败则尝试强制恢复
  }
}

/**
 * 删档重置逻辑
 */
async function handleReset() {
  const confirmed = window.confirm("⚠️ 确定要删档重置吗？\n所有等级、属性、步数加成将永久清空！");
  if (!confirmed) return;

  // 锁定状态，防止重置期间发生战斗计算
  gameState.isDead = true;

  try {
    const res = await axios.post('/reset');
    
    // 同步后端返回的初始数据
    gameState.player = res.data.player;
    gameState.enemy = res.data.monster;
    gameState.isDead = false;
    
    // UI 清空
    gameState.logs = []; 
    actions.addLog("✨ 时间线已重置，英雄重新启程！", "level-up");
    
    alert("重置成功！");
  } catch (e) {
    console.error("重置请求失败:", e);
    actions.addLog("❌ 重置失败，请联系管理员", "danger");
    gameState.isDead = false;
  }
}

onMounted(async () => {
  await actions.fetchStatus(); // 初始化加载数据
  startBattleLoop();           // 开启战斗齿轮
});
</script>

<style scoped>
.game-root {
  min-height: 100vh;
  background-color: #020617;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 0;
  color: #f8fafc;
  font-family: 'Inter', system-ui, sans-serif;
}

.game-container {
  width: 1100px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.main-content {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
}

.left-side {
  width: 420px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-side {
  flex: 1;
  max-width: 640px;
}

/* 战斗日志面板 */
.log-panel {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid #1e293b;
  border-radius: 16px;
  padding: 20px;
  height: 550px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.log-header {
  border-bottom: 1px solid #334155;
  padding-bottom: 12px;
  margin-bottom: 15px;
  font-size: 13px;
  color: #94a3b8;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  background: #22c55e;
  border-radius: 50%;
  margin-right: 8px;
  box-shadow: 0 0 8px #22c55e;
}

.log-body {
  flex: 1;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #334155 transparent;
}

.log-row {
  margin-bottom: 8px;
  padding: 10px 14px;
  background: rgba(255,255,255,0.03);
  border-left: 4px solid #475569;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.5;
}

/* 日志类型颜色 */
.info { border-left-color: #6366f1; color: #a5b4fc; }
.danger { border-left-color: #ef4444; color: #fca5a5; }
.success { border-left-color: #22c55e; color: #86efac; }
.level-up { border-left-color: #eab308; color: #fde047; font-weight: bold; }
.system { border-left-color: #94a3b8; color: #cbd5e1; font-style: italic; }

/* 经验条卡片 */
.xp-mini-card {
  background: #0f172a;
  border: 1px solid #1e293b;
  padding: 15px;
  border-radius: 12px;
}
.xp-info {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  margin-bottom: 8px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.xp-bar-bg { height: 8px; background: #020617; border-radius: 4px; overflow: hidden; }
.xp-bar-fill { height: 100%; background: linear-gradient(90deg, #4f46e5, #9333ea); transition: width 0.6s cubic-bezier(0.34, 1.56, 0.64, 1); }

.sync-button {
  background: #1e1b4b;
  border: 1px solid #4338ca;
  padding: 16px;
  border-radius: 12px;
  color: #c7d2fe;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}
.sync-button:hover { background: #312e81; box-shadow: 0 0 20px rgba(67, 56, 202, 0.4); }

/* 危险操作区 */
.danger-zone {
  margin-top: 10px;
  border-top: 1px solid #1e293b;
  padding-top: 20px;
}
.reset-button {
  width: 100%;
  background: rgba(127, 29, 29, 0.2);
  border: 1px solid #7f1d1d;
  padding: 12px;
  border-radius: 10px;
  color: #f87171;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
}
.reset-button:hover { background: #7f1d1d; color: white; }

/* 列表过渡动画 */
.list-enter-active, .list-leave-active { transition: all 0.5s ease; }
.list-enter-from { opacity: 0; transform: translateX(30px); }
</style>