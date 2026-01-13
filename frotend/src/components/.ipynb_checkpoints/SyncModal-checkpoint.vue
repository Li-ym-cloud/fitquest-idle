<template>
  <Transition name="fade">
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/90 backdrop-blur-md">
      <div class="bg-slate-900 border border-slate-700 rounded-3xl p-8 w-full max-w-sm shadow-2xl relative">
        <button 
          @click="$emit('close')" 
          class="absolute top-4 right-4 text-slate-500 hover:text-white transition-colors text-xl"
        >✕</button>
        
        <div class="text-center mb-6">
          <div class="text-5xl mb-4 drop-shadow-lg">⌚</div>
          <h3 class="text-xl font-bold text-white">同步健身数据</h3>
          <p class="text-slate-400 text-xs mt-2 italic">上传您的智能设备导出的 .json 步数记录</p>
        </div>

        <label class="group block w-full border-2 border-dashed border-slate-700 rounded-2xl p-10 text-center cursor-pointer hover:border-indigo-500 hover:bg-indigo-500/5 transition-all">
          <input type="file" class="hidden" @change="onFileChange" accept=".json" />
          <div class="flex flex-col items-center">
            <span class="text-indigo-400 group-hover:scale-110 transition-transform mb-2">点击选择文件</span>
            <span class="text-[10px] text-slate-500 tracking-widest uppercase">Max size: 1MB</span>
          </div>
        </label>

        <p class="mt-4 text-[9px] text-slate-600 text-center uppercase tracking-tighter">
          数据将通过安全加密通道同步至服务器
        </p>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import axios from 'axios';
import { gameState } from '../store/game';

// 定义通知父组件的事件
const emit = defineEmits(['close']);

async function onFileChange(e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = async (event) => {
    try {
      const jsonData = JSON.parse(event.target.result);
      // 调用后端同步接口
      const res = await axios.post('/api/sync-fitness', jsonData);
      
      // 更新全局状态中的点数
      gameState.player.points = res.data.points;
      
      // 成功提示并关闭弹窗
      alert(`🎉 ${res.data.message}`);
      emit('close');
    } catch (err) {
      console.error(err);
      alert("❌ 同步失败：请确保文件格式为正确的 JSON");
    }
  };
  reader.readAsText(file);
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: all 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: scale(0.95); }
</style>