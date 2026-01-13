<template>
  <div class="min-h-screen bg-gray-900 text-white p-6 font-mono">
    <div class="max-w-xl mx-auto grid grid-cols-3 gap-4 mb-8">
      <div v-for="(val, key) in statConfig" :key="key" class="bg-gray-800 p-4 rounded-lg border border-gray-700 text-center">
        <span class="text-xs text-gray-400">{{ val.label }}</span>
        <div class="text-2xl font-bold">{{ gameState.player[val.key] }}</div>
        <button 
          v-if="gameState.player.points > 0"
          @click="handleUpgrade(key)"
          class="mt-2 bg-green-600 hover:bg-green-500 text-xs px-3 py-1 rounded-full animate-pulse transition-transform active:scale-90"
        > +1 Point </button>
      </div>
    </div>

    <div class="relative h-64 bg-black rounded-2xl border-4 border-gray-800 flex items-center justify-around mb-6">
      <div :class="['text-6xl transition-all duration-100', gameState.isAttacking ? 'translate-x-10 scale-110' : '']">
        🤺
      </div>
      
      <transition name="float">
        <div v-if="gameState.damagePopup" class="absolute right-1/4 top-1/3 text-red-500 font-black text-2xl pointer-events-none">
          -{{ gameState.player.physical_atk }}
        </div>
      </transition>

      <div class="text-6xl flex flex-col items-center">
        <div class="w-20 bg-gray-700 h-2 rounded mb-2 overflow-hidden border border-gray-600">
          <div class="bg-red-600 h-full transition-all duration-200" :style="{width: (gameState.enemy.hp/gameState.enemy.maxHp)*100 + '%'}"></div>
        </div>
        👹
      </div>
    </div>

    <div class="max-w-xl mx-auto bg-gray-800 p-4 rounded-xl border border-gray-700">
      <div class="flex justify-between mb-2 items-end">
        <div>
          <span class="text-blue-400 font-bold text-xl">LV. {{ gameState.player.level }}</span>
          <span class="ml-2 text-xs text-gray-500">Available Points: {{ gameState.player.points }}</span>
        </div>
        <span class="text-gray-400 text-xs">EXP: {{ gameState.player.xp }} / {{ gameState.player.xp_next }}</span>
      </div>
      <div class="w-full bg-gray-700 h-3 rounded-full overflow-hidden">
        <div class="bg-blue-500 h-full transition-all duration-300" :style="{width: (gameState.player.xp / gameState.player.xp_next)*100 + '%'}"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { gameState, actions } from './store/game';
import axios from 'axios';

const statConfig = {
  physical: { label: '物理攻击', key: 'physical_atk' },
  magic: { label: '魔法攻击', key: 'magic_atk' },
  hp: { label: '最大血量', key: 'max_hp' }
};

// 处理加点逻辑
async function handleUpgrade(type) {
  try {
    await actions.addPoint(type);
  } catch (err) {
    console.error("加点失败:", err.response?.data?.detail || err.message);
  }
}

// 战斗循环逻辑
function startBattleLoop() {
  // 注意：将回调函数改为 async
  setInterval(async () => {
    // 1. 触发攻击动画
    gameState.isAttacking = true;
    gameState.damagePopup = true;
    
    // 2. 本地预计算伤害（让 UI 瞬间反馈）
    gameState.enemy.hp -= gameState.player.physical_atk;
    gameState.player.xp += 1;

    // 3. 升级判定
    if (gameState.player.xp >= gameState.player.xp_next) {
      console.log("检测到升级，正在同步后端...");
      try {
        // 修改点：调用专门的升级接口 /api/level-up
        const res = await axios.post('/api/level-up');
        // 使用后端返回的权威数据覆盖本地状态
        Object.assign(gameState.player, res.data);
      } catch (err) {
        console.error("升级同步失败，请检查网络");
      }
    }

    // 4. 重置动画状态
    setTimeout(() => {
      gameState.isAttacking = false;
      gameState.damagePopup = false;
    }, 200);

    // 5. 敌人刷新逻辑
    if (gameState.enemy.hp <= 0) {
      gameState.enemy.maxHp = Math.floor(gameState.enemy.maxHp * 1.2) + 10;
      gameState.enemy.hp = gameState.enemy.maxHp;
    }
  }, 1000);
}

onMounted(() => {
  actions.fetchStatus();
  startBattleLoop();
});
</script>

<style>
/* 伤害数字弹出动画 */
.float-enter-active {
  animation: float-up 0.6s ease-out;
}

@keyframes float-up {
  0% { transform: translateY(0) scale(1); opacity: 1; }
  50% { transform: translateY(-30px) scale(1.2); opacity: 1; }
  100% { transform: translateY(-60px) scale(1); opacity: 0; }
}
</style>