<template>
  <div class="max-w-xl mx-auto bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-lg">
    <div class="flex justify-between mb-2 items-end">
      <div>
        <span class="text-blue-400 font-bold text-xl tracking-tighter">LV. {{ gameState.player.level }}</span>
        <span v-if="gameState.player.points > 0" class="ml-3 text-[10px] text-yellow-500 animate-pulse uppercase">
          ● {{ gameState.player.points }} Point(s) Available
        </span>
      </div>
      <span class="text-slate-500 text-[10px] font-mono">
        EXP: {{ gameState.player.xp }} / {{ gameState.player.xp_next }}
      </span>
    </div>

    <div class="w-full bg-slate-900 h-3 rounded-full overflow-hidden border border-slate-700 p-0.5">
      <div 
        class="bg-gradient-to-r from-blue-600 to-indigo-400 h-full rounded-full transition-all duration-500 ease-out shadow-[0_0_8px_rgba(59,130,246,0.5)]" 
        :style="{ width: (gameState.player.xp / gameState.player.xp_next) * 100 + '%' }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { gameState } from '../store/game';
</script>