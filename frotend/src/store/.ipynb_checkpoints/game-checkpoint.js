import { reactive } from 'vue';
import axios from 'axios';

export const gameState = reactive({
    player: {}, // 从后端获取
    enemy: { hp: 50, maxHp: 50 },
    isAttacking: false,
    damagePopup: null // 用于展示伤害数字
});

export const actions = {
    async fetchStatus() {
        const res = await axios.get('/api/game-status');
        gameState.player = res.data;
    },
    async addPoint(type) {
        const res = await axios.post(`/api/upgrade?stat_type=${type}`);
        gameState.player = res.data;
    }
};