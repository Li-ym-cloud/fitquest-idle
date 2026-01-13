<template>
  <header class="bg-slate-900 border-b-4 border-indigo-500 p-6 rounded-t-2xl shadow-2xl flex justify-between">
    <div>
      <h1 class="text-3xl font-black text-indigo-400 italic">FITQUEST</h1>
      <p class="text-xs text-slate-500 mt-1 uppercase tracking-widest">Points: {{ gameState.player.points }}</p>
    </div>
    <div class="flex gap-4">
      <div v-for="(val, key) in statConfig" :key="key" class="text-center">
        <div class="text-[10px] text-slate-500 uppercase">{{ val.label }}</div>
        <div class="font-bold flex items-center gap-1">
          {{ gameState.player[val.key] }}
          <button v-if="gameState.player.points > 0" @click="actions.addPoint(key)" class="text-indigo-400 hover:text-white">+</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { gameState, actions } from '../store/game';
const statConfig = {
  physical: { label: 'ATK', key: 'physical_atk' },
  magic: { label: 'MAG', key: 'magic_atk' },
  hp: { label: 'HP', key: 'max_hp' }
};
</script>