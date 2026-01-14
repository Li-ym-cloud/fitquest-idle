<template>
  <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl relative overflow-hidden">
    <div class="absolute -top-2 -right-2 p-4 opacity-5 text-6xl font-black italic">
        <span class="text-[10px] text-slate-400 font-bold uppercase">冒险者等级:</span>
      {{ gameState.player.level }}
    </div>

    <div class="relative z-10 space-y-5">
      <div class="flex justify-between items-start">
        <div>
          <h2 class="text-2xl font-black text-white italic tracking-tighter uppercase">
            {{ gameState.player.name }}
          </h2>
          <div class="flex items-center gap-2 mt-1">
            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            <span class="text-[10px] text-slate-400 font-bold uppercase">在线冒险者</span>
          </div>
        </div>
        <div class="text-right">
          <p class="text-[9px] text-slate-500 uppercase">可用属性点</p>
          <p class="text-xl font-mono text-yellow-500 font-bold leading-none">{{ gameState.player.points }}</p>
        </div>
      </div>

      <div class="space-y-2 bg-slate-950/40 p-3 rounded-xl border border-white/5">
        <div class="flex justify-between items-center mb-1">
          <span class="text-[10px] font-bold text-red-400 uppercase tracking-tighter">生命值 (HP)</span>
          <span class="text-xs font-mono font-bold text-white">
            {{ Math.max(0, gameState.player.current_hp) }} / {{ gameState.player.max_hp }}
          </span>
        </div>
        <button v-if="gameState.player.points > 0" @click="actions.addPoint('hp')" 
                  class="w-7 h-7 bg-indigo-600 hover:bg-indigo-500 rounded-lg flex items-center justify-center text-white font-bold transition-all active:scale-90 shadow-lg">+ </button>
        <div class="h-3 bg-slate-900 rounded-full border border-slate-800 p-0.5">
          <div class="h-full bg-gradient-to-r from-red-600 to-orange-500 rounded-full transition-all duration-500 shadow-[0_0_10px_rgba(239,68,68,0.3)]"
               :style="{ width: (gameState.player.current_hp / gameState.player.max_hp * 100) + '%' }">
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="bg-slate-950/80 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
          <div>
            <span class="text-[9px] text-slate-500 block uppercase">物理攻击</span>
            <span class="text-xl font-bold text-slate-200">{{ gameState.player.physical_atk }}</span>
          </div>
          <button v-if="gameState.player.points > 0" @click="actions.addPoint('physical')" 
                  class="w-7 h-7 bg-indigo-600 hover:bg-indigo-500 rounded-lg flex items-center justify-center text-white font-bold transition-all active:scale-90 shadow-lg">+ </button>
        </div>

        <div class="bg-slate-950/80 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
          <div>
            <span class="text-[9px] text-slate-500 block uppercase">魔法攻击</span>
            <span class="text-xl font-bold text-slate-200">{{ gameState.player.magic_atk }}</span>
          </div>
          <button v-if="gameState.player.points > 0" @click="actions.addPoint('magic')" 
                  class="w-7 h-7 bg-indigo-600 hover:bg-indigo-500 rounded-lg flex items-center justify-center text-white font-bold transition-all active:scale-90 shadow-lg">+ </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { gameState, actions } from '../store/game';
</script>