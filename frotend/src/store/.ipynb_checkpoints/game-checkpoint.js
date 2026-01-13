import { reactive } from 'vue';
import axios from 'axios';

axios.defaults.baseURL = `http://${window.location.hostname}:8000`;

export const gameState = reactive({
  player: { name: "Hero", level: 1, xp: 0, xp_next: 10, points: 0, current_hp: 100, max_hp: 100, death_count: 0 },
  enemy: { name: "寻找中...", hp: 0, max_hp: 0, level: 1 },
  logs: [],
  isAttacking: false,
  isDead: false
});

export const actions = {
  async fetchStatus() {
    console.log("[前端日志] 正在执行 fetchStatus...");
    try {
      const res = await axios.get('/game-status');
      gameState.player = res.data.player;
      gameState.enemy = res.data.monster;
      console.log("[前端日志] fetchStatus 成功同步, 当前 XP:", gameState.player.xp);
    } catch (e) {
      console.error("[前端日志] fetchStatus 失败:", e);
    }
  },

 async addPoint(type) {
    if (gameState.player.points <= 0) return;

    try {
      // 调用后端的 upgrade 接口
      const res = await axios.post(`/upgrade?stat_type=${type}`);
      
      // 用后端返回的最新数据更新本地状态
      gameState.player = res.data; 
      
      this.addLog(`✨ 属性提升成功！`, 'success');
    } catch (e) {
      console.error("加点失败:", e);
      this.addLog("加点失败，请稍后再试", "danger");
    }
  },

  addLog(msg, type = 'info') {
    const time = new Date().toTimeString().split(' ')[0];
    gameState.logs.unshift({ id: Date.now() + Math.random(), time, msg, type });
    if (gameState.logs.length > 10) gameState.logs.pop();
  },

  // --- 关键修复：确保这个方法被调用 ---
  async handleMonsterDefeat() {
    console.log("[前端日志] >>> 触发 handleMonsterDefeat <<<");
    try {
      console.log("[前端日志] 准备请求 /add-xp...");
      const resXp = await axios.post('/add-xp?amount=2');
      
      console.log("[前端日志] /add-xp 响应成功, 后端返回 XP:", resXp.data.xp);
      
      // 更新本地内存
      gameState.player.xp = resXp.data.xp;
      gameState.player.current_hp = resXp.data.current_hp;
      
      this.addLog(`🏆 战胜对手，经验+2`, 'success');

      if (gameState.player.xp >= gameState.player.xp_next) {
        console.log("[前端日志] 经验已满，请求 /level-up...");
        const resLv = await axios.post('/level-up');
        gameState.player = resLv.data.player;
        gameState.enemy = resLv.data.monster;
        this.addLog(`🌟 升级了！当前 LV.${gameState.player.level}`, 'level-up');
      } else {
        console.log("[前端日志] 经验未满，请求新怪物...");
        await this.fetchStatus();
      }
    } catch (e) {
      console.error("[前端日志] handleMonsterDefeat 执行过程报错:", e);
    }
  }
};