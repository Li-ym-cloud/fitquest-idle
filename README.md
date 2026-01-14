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
```
![结果展示](./Snipaste_2026-01-13_18-56-25.png)

# 📱 iPhone 运动数据同步方案

本方案利用 iOS 自带的 **“快捷指令 (Shortcuts)”** 功能，实现无需开发原生 App 即可将 iPhone 健康数据（HealthKit）同步至游戏后端，并根据步数发放游戏内奖励。

---

## 1. 后端接口实现 (FastAPI)

在 `main.py` 中添加数据模型与接收接口。

```python
from pydantic import BaseModel

# 定义步数同步数据模型
class SyncData(BaseModel):
    steps: int

@app.post("/sync-steps")
async def sync_steps(data: SyncData):
    global db_player
    
    # --- 奖励逻辑设计 ---
    # 示例：每 2000 步奖励 1 个属性点
    reward = data.steps // 2000
    
    if reward > 0:
        db_player.points += reward
        # 执行持久化存储
        save_player(db_player)
        
    return {
        "status": "success", 
        "reward_points": reward, 
        "total_points": db_player.points,
        "synced_steps": data.steps
    }
```
---

## 一、后端业务处理流程

### 1. 数据接收
后端开放专用 API sync-steps 接口，用于监听并接收来自移动端上报的步数统计数据。

### 2. 奖励换算
服务器在获取步数后，按照预设规则进行奖励计算，例如：
- 每 2000 步兑换 1 点属性点

### 3. 状态同步
- 将计算得到的奖励点数累加至玩家当前的可用属性点池  
- 同步触发数据持久化逻辑，确保数据库与内存状态保持一致

### 4. 接口反馈
向移动端返回处理结果，包括：
- 同步是否成功  
- 本次获得的奖励点数  
- 更新后的玩家总属性点数

---

## 二、iOS 快捷指令配置流程（移动端）

### 1. 步数采集阶段
- **健康样本检索**：读取 iOS 健康 App 中的「步数」数据  
- **时间范围设定**：统计区间设置为「过去 24 小时」  
- **统计汇总**：对多个时间片段的步数数据执行求和，得到单日总步数

### 2. 网络传输阶段
- **目标地址配置**：指定游戏服务器的接口 URL  
- **请求封装**：将单日步数封装为标准 JSON 数据  
- **指令发送**：通过 POST 请求将数据传输至服务器端

---

## 三、自动化执行逻辑

### 1. 触发机制设定
- **定时触发**：建议每日 23:30 自动执行，保证全天步数统计完整  
- **事件触发**：可设置为关闭指定 App、或连接充电器时自动执行

### 2. 静默运行配置
- 关闭「运行前询问」选项  
- 开启「运行时不显示」，确保同步流程在后台完成，不打断用户操作

---

## 四、核心保障与说明事项

### 1. 网络环境要求
- **局域网测试**：iPhone 与服务器需位于同一 Wi-Fi 网络  
- **远程同步**：需使用内网穿透方案或部署公网服务器 IP

### 2. 数据权威性
快捷指令直接调用 iOS 健康系统接口，数据来源于设备硬件传感器，真实性和可靠性较高。

### 3. 风险防范
建议在后端增加安全控制策略，例如：
- 每日同步次数限制  
- 单日可获得奖励点数上限  

用于防止异常数据或恶意刷取行为。

---

**文档用途建议**：  
- 技术方案设计说明  
- 游戏数值系统与健康数据融合方案  
- 产品/研发对齐用流程文档

