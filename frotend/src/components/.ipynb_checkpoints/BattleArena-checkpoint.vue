<template>
  <section class="relative h-64 bg-slate-900 rounded-2xl border border-slate-700 flex items-center justify-around overflow-hidden shadow-inner">
    <div :class="['text-7xl transition-all duration-100 z-10', gameState.isAttacking ? 'translate-x-12 rotate-12' : '']">
      🤺
    </div>
    
    <transition name="damage">
      <div v-if="gameState.damagePopup" class="absolute right-1/4 top-1/4 text-red-500 font-black text-4xl italic z-20">
        -{{ gameState.player.physical_atk }}
      </div>
    </transition>

    <div class="flex flex-col items-center z-10">
      <div class="w-24 bg-slate-800 h-2 rounded-full mb-4 border border-slate-700 overflow-hidden">
        <div class="bg-red-500 h-full transition-all" :style="{width: (gameState.enemy.hp/gameState.enemy.maxHp)*100 + '%'}"></div>
      </div>
      <span class="text-7xl">👹</span>
    </div>
  </section>
</template>

<script setup>
import { gameState } from '../store/game';
</script>

<style scoped>
.damage-enter-active { animation: damage-pop 0.6s cubic-bezier(0.18, 0.89, 0.32, 1.28); }
@keyframes damage-pop {
  0% { transform: translateY(0) scale(0.5); opacity: 0; }
  30% { transform: translateY(-20px) scale(1.5); opacity: 1; }
  100% { transform: translateY(-50px) scale(1); opacity: 0; }
}
</style>