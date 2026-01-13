import { reactive } from 'vue';
import axios from 'axios';

// --- 通用适配逻辑 ---
// 获取当前浏览器访问的域名/IP (例如: 192.168.102.40 或 localhost)
const currentHost = window.location.hostname;

axios.defaults.baseURL = `http://${currentHost}:8000`;

export const gameState = reactive({
  player: { 
    name: "Hero", level: 1, xp: 0, xp_next: 10, points: 0, 
    current_hp: 100, max_hp: 100, physical_atk: 5, magic_atk: 2,
    death_count: 0 
  },
  enemy: { name: "寻找中...", hp: 0, max_hp: 0, physical_atk: 0, level: 1 },
  logs: [],
  isAttacking: false,
  isDead: false
});

export const actions = {
  addLog(msg, type = 'info') {
    const time = new Date().toTimeString().split(' ')[0];
    gameState.logs.unshift({ id: Date.now(), time, msg, type });
    if (gameState.logs.length > 10) gameState.logs.pop();
  },
  async fetchStatus() {
    try {
      const res = await axios.get('/game-status');
      gameState.player = res.data.player;
      gameState.enemy = res.data.monster;
      gameState.player.death_count = res.data.death_count;
    } catch (e) { console.error("连接失败"); }
  }
};