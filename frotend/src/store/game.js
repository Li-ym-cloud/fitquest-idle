import { reactive } from 'vue';
import axios from 'axios';

// 基础配置：确保指向 FastAPI 默认端口 8000
axios.defaults.baseURL = `http://${window.location.hostname}:8000`;

/**
 * 游戏全局状态存储
 */
export const gameState = reactive({
  player: { 
    name: "Hero", 
    level: 1, 
    xp: 0, 
    xp_next: 10, 
    points: 0, 
    current_hp: 100, 
    max_hp: 100, 
    physical_atk: 5, 
    magic_atk: 2, 
    death_count: 0 
  },
  enemy: { 
    name: "正在寻找对手...", 
    hp: 0, 
    max_hp: 0, 
    level: 1, 
    physical_atk: 0 
  },
  logs: [],
  isAttacking: false,
  isDead: false
});

/**
 * 游戏核心交互动作
 */
export const actions = {
  /**
   * 1. 基础状态同步 (从后端获取最新数据)
   */
  async fetchStatus() {
    try {
      const res = await axios.get('/game-status');
      gameState.player = res.data.player;
      gameState.enemy = res.data.monster;
    } catch (e) {
      console.error("[通讯错误] 无法获取游戏状态:", e);
    }
  },

  /**
   * 2. 怪物战胜处理逻辑 (核心修复)
   */
  async handleMonsterDefeat() {
    console.log("[战斗结算] 怪物已倒下，正在结算奖励...");
    try {
      // 第一步：发送击杀请求，后端会增加 XP
      const resXp = await axios.post('/add-xp?amount=2');
      
      // 第二步：判断是否需要升级
      // 注意：后端的 level-up 逻辑会自动重置 xp 和生成新怪
      if (resXp.data.xp >= resXp.data.xp_next) {
        this.addLog("🌟 经验已满，正在突破等级...", "system");
        const resLv = await axios.post('/level-up');
        gameState.player = resLv.data.player;
        gameState.enemy = resLv.data.monster;
        this.addLog(`🎊 升级了！当前 LV.${gameState.player.level}`, 'level-up');
      } else {
        // 第三步：未升级则调用 game-status
        // 后端的 get_status 会因为 db_monster.hp <= 0 而触发 apply_dynamic_nerf
        const resStatus = await axios.get('/game-status');
        gameState.player = resStatus.data.player;
        gameState.enemy = resStatus.data.monster;
        this.addLog(`🏆 战斗胜利！经验 +2`, 'success');
      }
    } catch (e) {
      console.error("[结算异常]", e);
      this.addLog("结算请求超时，请检查网络", "danger");
    }
  },

  /**
   * 3. 属性加点逻辑
   * 支持类型: 'physical', 'magic', 'hp'
   */
  async addPoint(type) {
    if (gameState.player.points <= 0) {
      this.addLog("属性点不足", "system");
      return;
    }
    try {
      const res = await axios.post(`/upgrade?stat_type=${type}`);
      gameState.player = res.data; 
      const label = type === 'hp' ? '生命上限' : (type === 'physical' ? '物理攻击' : '魔法攻击');
      this.addLog(`✨ ${label} 提升成功！`, 'success');
    } catch (e) {
      console.error("加点失败:", e);
    }
  },

  /**
   * 4. 辅助：添加战斗日志
   */
  addLog(msg, type = 'info') {
    const time = new Date().toTimeString().split(' ')[0];
    gameState.logs.unshift({ 
      id: Date.now() + Math.random(), 
      time, 
      msg, 
      type 
    });
    // 限制日志条数，保持界面整洁
    if (gameState.logs.length > 8) gameState.logs.pop();
  }
};