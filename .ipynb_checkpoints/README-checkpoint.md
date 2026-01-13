# FitQuest Idle: 健身远征

> **让每一滴汗水都化为一次暴击。**
> FitQuest Idle 是一款开源的健身驱动型挂机游戏，旨在将用户的真实运动数据（如 Apple Watch 拳击计数、每日步数）转化为游戏内角色的成长动力。

---

## 📂 项目结构 (Project Structure)

本项目采用前后端分离架构，核心目录规划如下：

| 目录/文件 | 作用描述 | MD5 校验 (Initial) |
| :--- | :--- | :--- |
| **`/backend`** | **后端核心**：基于 FastAPI，负责核心逻辑计算与 API 接口。 | - |
| ├── `/api` | 路由定义。如健身同步 (`/sync-fitness`)、状态获取 (`/game-status`)。 | - |
| ├── `/core` | **游戏大脑**：包含数值转换公式 (Fitness-to-RPG) 与 Tick 定时器。 | - |
| └── `/models` | 数据模型：定义玩家存档、健身记录、角色属性的数据库结构。 | - |
| **`/frontend`** | **前端展示**：基于 Vue.js (推荐) 或 React 的挂机界面。 | - |
| ├── `/src/assets` | 静态资源：角色图标、UI 素材、背景音乐及 CSS 动画。 | - |
| └── `/src/store` | 状态管理 (Pinia/Redux)：实时同步后端跳动的金币与经验值。 | - |
| **`/data`** | **模拟数据**：存放本地开发测试用的 JSON 健身样本数据。 | `5d41402abc4...` |
| **`/docs`** | **项目文档**：包含 API 协议规范、详细算法说明及开发手册。 | - |

---

## ⚙️ 核心逻辑：健身数据转化 (Conversion Algorithm)

游戏通过特定的转换模型将现实能量注入虚拟世界：

$$Character\_Power = (Steps \times 0.01) + (Punch\_Count \times 0.5)$$

* **步数 (Steps)**：每 100 步增加 1 点基础体力。
* **出拳数 (Punch Count)**：每一拳增加 0.5 点爆发伤害。
* **离线收益**：根据最近 24 小时的运动消耗量计算离线金币加成倍率。

---

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone [https://github.com/your-username/fitquest-idle.git](https://github.com/your-username/fitquest-idle.git)
cd fitquest-idle