<template>
  <div class="arena-container">
    <div class="monster-card" v-if="gameState.enemy.name">
      <div class="m-header">
        <span class="m-badge">LV.{{ gameState.enemy.level }}</span>
        <span class="m-name">{{ gameState.enemy.name }}</span>
      </div>
      <div class="m-hp-box">
        <div class="m-hp-bar" :style="{ width: hpBarWidth + '%' }"></div>
        <span class="m-hp-text">{{ gameState.enemy.hp }} / {{ gameState.enemy.max_hp }}</span>
      </div>
      <div class="m-atk-tag">攻击力: {{ gameState.enemy.physical_atk }}</div>
    </div>

    <div class="battle-view">
      <div class="actor player" :class="{ 'attack-anim': gameState.isAttacking }">🛡️</div>
      <div class="vs-text">VS</div>
      <div class="actor monster">👹</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { gameState } from '../store/game';

const hpBarWidth = computed(() => {
  if (!gameState.enemy.max_hp) return 0;
  return (gameState.enemy.hp / gameState.enemy.max_hp) * 100;
});
</script>

<style scoped>
.arena-container {
  background: #0f172a;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #334155;
}
.monster-card {
  max-width: 300px;
  margin: 0 auto 20px;
  text-align: center;
}
.m-header { display: flex; justify-content: center; gap: 8px; margin-bottom: 8px; }
.m-badge { background: #eab308; color: #000; font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 4px; }
.m-name { font-weight: bold; color: #f1f5f9; }
.m-hp-box { height: 16px; background: #020617; border-radius: 8px; position: relative; overflow: hidden; border: 1px solid #1e293b; }
.m-hp-bar { height: 100%; background: #ef4444; transition: width 0.3s; }
.m-hp-text { position: absolute; top:0; left:0; width:100%; font-size: 10px; line-height: 14px; color: white; text-shadow: 1px 1px 1px black; }
.m-atk-tag { font-size: 11px; color: #fca5a5; margin-top: 4px; }
.battle-view { display: flex; justify-content: space-around; align-items: center; padding: 20px 0; }
.actor { font-size: 40px; transition: transform 0.1s; }
.attack-anim { transform: translateX(30px); }
.vs-text { font-weight: 900; color: #475569; }
</style>