<template>
  <div class="min-h-screen bg-slate-950 text-slate-200 p-4 font-mono">
    <div class="max-w-2xl mx-auto space-y-6">
      <StatPanel />

      <BattleArena />

      <div class="grid grid-cols-2 gap-4">
        <div class="bg-slate-900 p-4 rounded-2xl border border-slate-800">
           <p class="text-xs text-slate-500 text-center mt-4 uppercase">Battle Mode: Auto</p>
        </div>
        
        <div class="bg-indigo-900/20 border border-indigo-500/30 rounded-2xl p-6 text-center cursor-pointer hover:bg-indigo-900/30"
             @click="showModal = true">
          <div class="text-4xl">⌚</div>
          <span class="text-indigo-300 font-bold text-xs uppercase">Sync Watch</span>
        </div>
      </div>

      <XPBar />

      <SyncModal v-if="showModal" @close="showModal = false" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { gameState, actions } from './store/game';
import axios from 'axios';

// 导入拆分后的组件
import StatPanel from './components/StatPanel.vue';
import BattleArena from './components/BattleArena.vue';
import XPBar from './components/XPBar.vue';
import SyncModal from './components/SyncModal.vue';

const showModal = ref(false);

// 战斗循环逻辑（保持在 App 层或移至 store）
function startBattleLoop() {
  setInterval(async () => {
    gameState.isAttacking = true;
    gameState.damagePopup = true;
    gameState.enemy.hp -= gameState.player.physical_atk;
    gameState.player.xp += 1;

    if (gameState.player.xp >= gameState.player.xp_next) {
      const res = await axios.post('/api/level-up');
      Object.assign(gameState.player, res.data);
    }

    setTimeout(() => {
      gameState.isAttacking = false;
      gameState.damagePopup = false;
    }, 200);

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