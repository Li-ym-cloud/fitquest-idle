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
        </div>

        <div class="right-side">
          <div class="log-panel">
            <div class="log-header">
              <span class="dot"></span> 实时战斗记录
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
import { ref, onMounted } from 'vue';
import { gameState, actions } from './store/game';
import axios from 'axios';
import StatPanel from './components/StatPanel.vue';
import BattleArena from './components/BattleArena.vue';
import SyncModal from './components/SyncModal.vue';

const showModal = ref(false);

// 自动打怪逻辑
// 核心战斗循环：修复自动打怪
function startBattleLoop() {
  console.log("战斗系统：尝试启动...");
  
  const timer = setInterval(async () => {
    // 调试日志：如果没攻击，可以在控制台看这里输出了什么
    // console.log("当前敌人状态:", gameState.enemy.name, "HP:", gameState.enemy.hp);

    // 判定条件：
    // 1. 玩家不能是死亡状态
    // 2. 怪物必须有名字且血量大于 0
    if (gameState.isDead) return;
    if (!gameState.enemy || !gameState.enemy.name || gameState.enemy.name === "寻找中..." || gameState.enemy.hp <= 0) {
      return;
    }

    // --- 开始攻击逻辑 ---
    gameState.isAttacking = true;

    // 1. 玩家对怪物造成伤害
    const pDmg = gameState.player.physical_atk + gameState.player.magic_atk;
    gameState.enemy.hp -= pDmg;
    actions.addLog(`⚔️ 你发动攻击，造成了 ${pDmg} 点伤害`, 'info');

    // 2. 怪物反击 (延迟 400ms 增加打击感)
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

    // 3. 检查怪物是否死亡
    if (gameState.enemy.hp <= 0) {
      await handleMonsterDefeat();
    }
  }, 1600); // 1.6秒为一个回合
}

onMounted(async () => {
  // 关键：必须先 await 拿到数据，否则 startBattleLoop 进去时 hp 还是 0
  await actions.fetchStatus(); 
  startBattleLoop();
});

async function handleMonsterDefeat() {
  actions.addLog(`胜利！击败了 [${gameState.enemy.name}]`, 'success');
  // 这里可以发请求给后端增加经验，或者前端先加
  gameState.player.xp += 2; 
  if (gameState.player.xp >= gameState.player.xp_next) {
    const res = await axios.post('/level-up');
    gameState.player = res.data.player;
    gameState.enemy = res.data.monster;
    actions.addLog(`🌟 等级提升至 LV.${gameState.player.level}`, 'level-up');
  } else {
    // 刷一只新怪
    const res = await axios.get('/game-status');
    gameState.enemy = res.data.monster;
  }
}

async function triggerDeath() {
  gameState.isDead = true;
  gameState.player.current_hp = 0;
  actions.addLog(`❌ 战败！累计死亡 ${gameState.player.death_count + 1} 次，削弱怪物属性...`, "system");

  setTimeout(async () => {
    const res = await axios.post('/respawn');
    gameState.player = res.data.player;
    gameState.enemy = res.data.monster;
    gameState.isDead = false;
    actions.addLog(`🛡️ 复活成功，继续战斗。`, 'success');
  }, 5000); // 5秒后复活
}

onMounted(() => {
  actions.fetchStatus();
  startBattleLoop();
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
}

.game-container {
  width: 1100px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.main-content {
  display: flex;
  flex-direction: row; /* 强制左右 */
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

/* 战斗日志样式 */
.log-panel {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid #1e293b;
  border-radius: 16px;
  padding: 20px;
  height: 500px;
  display: flex;
  flex-direction: column;
}

.log-header {
  border-bottom: 1px solid #334155;
  padding-bottom: 12px;
  margin-bottom: 15px;
  font-size: 13px;
  color: #94a3b8;
  display: flex;
  justify-content: space-between;
}

.log-body {
  flex: 1;
  overflow: hidden;
}

.log-row {
  margin-bottom: 8px;
  padding: 10px;
  background: rgba(0,0,0,0.2);
  border-left: 4px solid #475569;
  border-radius: 4px;
  font-size: 14px;
}

.info { border-left-color: #6366f1; color: #a5b4fc; }
.danger { border-left-color: #ef4444; color: #fca5a5; }
.success { border-left-color: #22c55e; color: #86efac; }
.level-up { border-left-color: #eab308; color: #fde047; }
.system { border-left-color: #94a3b8; color: #cbd5e1; font-style: italic; }

/* 经验条样式 */
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
  color: #64748b;
}
.xp-bar-bg { height: 6px; background: #020617; border-radius: 3px; overflow: hidden; }
.xp-bar-fill { height: 100%; background: #6366f1; transition: width 0.5s; }

.sync-button {
  background: #1e1b4b;
  border: 1px solid #4338ca;
  padding: 14px;
  border-radius: 12px;
  color: #c7d2fe;
  cursor: pointer;
}
</style>