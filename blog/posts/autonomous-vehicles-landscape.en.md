> By mid-2026, covering the two major tracks of unmanned delivery vehicles and Robotaxi

## 1. Overview of the two major tracks



```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        无人驾驶商业化两大赛道                                  │
├────────────────────────────────┬─────────────────────────────────────────────┤
│                                │                                             │
│   无人配送车                    │   Robotaxi (无人驾驶出租车)                  │
│   (低速 / 末端物流)             │   (高速 / 载人出行)                          │
│                                │                                             │
│   时速: ≤25km/h                │   时速: ≤120km/h                            │
│   场景: 园区/社区/街道          │   场景: 城市道路/高速公路                     │
│   等级: L4 (限定域)             │   等级: L4 (城市全域)                        │
│   成本: 1.6-20万/台             │   成本: 20-50万/台                          │
│   规模: 2025上半年 1.2万台交付  │   规模: 全球数千台运营                       │
│                                │                                             │
│   代表: 新石器/九识/白犀牛      │   代表: Waymo/萝卜快跑/小马/文远             │
│         美团/京东/菜鸟           │         特斯拉                              │
└────────────────────────────────┴─────────────────────────────────────────────┘
```



---

## 2. Unmanned delivery vehicle

### 2.1 Market Current Situation

| Indicators | Data |
|------|------|
| Shipments in 2024 | ~6,000 units |
| Delivery volume in the first half of 2025 | **>12,000 units** (double year-on-year) |
| Open right-of-way cities | **Over 200 cities**, 31 provinces |
| Vehicle Price Trend | 200,000-300,000 in 2021 → **16,000-50,000** in 2025 (>80% decrease) |
| Financing from January to May 2025 | More than 20 cases, unmanned delivery accounts for more than half |
| Forecast market size | Global **1.118 billion in 2026**; potential space ~500 billion yuan |

### 2.2 Leading companies

| Enterprise | Cumulative Deliveries/Operations | Latest News in 2025 | Selling Price |
|------|-------------|-------------|------|
| **Neolithic** | >15,000 units | Series D financing of 600 million+ US dollars; orders exceeding 20,000 units; No. 1 in global L4 distribution deployment | ~50,000 |
| **Jiushi Intelligence** | 15,000 units | Series B USD 400 million; covering 300+ cities; exported to Singapore/Japan, Korea/Middle East | **E6 naked car 19,800** |
| **White Rhino** | 2,000+ units | Series B 200 million yuan; operating in 170+ cities; 20 times growth in two years | ~30,000-50,000 |
| **JD Logistics** | Thousand units level | Self-developed unmanned light truck VAN; Lone Wolf series; 30-city trial operation | — |
| **Meituan** | Thousand units level | Normal operation in the core area of Shenzhen; self-developed delivery vehicles | — |
| **Rookie** | — | GT-Lite after stacking discounts **16,800** | 16,800 |
| **Hao Mo Zhixing** | — | Logistics/security/cleaning multi-scenario large orders | — |

### 2.3 Chip and computing platform

| Enterprise | Chip solution | Computing power | Sensor configuration |
|------|----------|------|-----------|
| **Neolithic** | NVIDIA Orin | 254 TOPS | 12 HD cameras + 1 LiDAR |
| **White Rhino** | NVIDIA Orin (single) | 254 TOPS | Matrix Domain Control + Sagitar LiDAR |
| **Youjia Innovation (Xiaozhu)** | Horizon J6M × 2 | ~200 TOPS | Tengjuchuang LiDAR + NavInfo P-BOX |
| **Xingshen Intelligence** | Horizon Journey 6M × 2 | ~200 TOPS | Multi-camera + Ultrasound |
| **Jiushi Intelligence** | — (Ultimate cost reduction) | — | Mainly camera + ultrasound |

### 2.4 General architecture of unmanned delivery vehicles



```
┌──────────────────────────────────────────────────────────────────────────┐
│                       无人配送车系统架构                                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌── 感知层 ──────────────────────────────────────────────────────────┐ │
│  │  摄像头 ×4-12 (360°环视)                                          │ │
│  │  激光雷达 ×0-1 (前向/顶部, 120m)                                  │ │
│  │  超声波 ×4-8 (近距避障, 0.2-6m)                                   │ │
│  │  毫米波雷达 ×0-2 (可选)                                           │ │
│  │  IMU + GNSS + 轮速计 (定位)                                       │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│         │                                                                │
│         ▼                                                                │
│  ┌── 计算平台 ────────────────────────────────────────────────────────┐ │
│  │                                                                    │ │
│  │  ┌─────────────────────┐     ┌──────────────────────────────┐    │ │
│  │  │ 主计算单元            │     │ 安全 MCU                      │    │ │
│  │  │ (Orin / 征程6M)      │     │ (功能安全冗余)                │    │ │
│  │  │                     │     │                              │    │ │
│  │  │ ├── 感知: BEV/OCC   │     │ 紧急制动 / 最小风险状态      │    │ │
│  │  │ ├── 规划: 路径/行为  │     │                              │    │ │
│  │  │ ├── 控制: 横纵向    │     └──────────────────────────────┘    │ │
│  │  │ └── 定位: 融合定位  │                                         │ │
│  │  └─────────────────────┘                                         │ │
│  │                                                                    │ │
│  │  OS: Linux (Ubuntu/ROS2)                                          │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│         │                                                                │
│         ▼                                                                │
│  ┌── 执行层 ──────────────────────────────────────────────────────────┐ │
│  │  线控底盘 (转向/驱动/制动)                                         │ │
│  │  货箱控制 (开门/锁定/温控)                                         │ │
│  │  交互屏幕 (取货码/状态显示)                                        │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│         │                                                                │
│         ▼                                                                │
│  ┌── 云端 ────────────────────────────────────────────────────────────┐ │
│  │  远程监控 / 远程接管 (Teleop)                                      │ │
│  │  车队调度 / 订单分配 / 路径规划                                     │ │
│  │  OTA 升级 / 数据回传 / 仿真训练                                    │ │
│  │  4G/5G + V2X 通信                                                  │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```



### 2.5 Cost reduction trend



```
价格演变 (L4 无人配送车):

2021年   ████████████████████████████████  20-30万
2023年   ████████████████                  8-10万
2024年   ████████                          4-5万
2025年   ████                              1.6-2万 (九识E6/菜鸟GT-Lite)

降本路径:
├── 芯片: 多颗激光雷达专用芯片 → 单颗 Orin/征程6M 通用 SoC
├── 激光雷达: 5颗机械式(10万+) → 1颗固态(2000-5000元) → 纯视觉(0)
├── 底盘: 定制底盘(5万+) → 微型电动车平台(1-2万)
├── 量产: 小批手工 → 产线自动化 (新石器万台下线)
└── 算法: 规则驱动 → 端到端神经网络 (减少工程量)
```



---

## 3. Robotaxi (unmanned taxi)

### 3.1 Global Competition Landscape

| Enterprise | Operation scale | Accumulated orders | Cities covered | Status |
|------|---------|---------|---------|------|
| **Waymo** | ~2,500 units | 20 million+ times | San Francisco/LA/Phoenix/Austin/Atlanta | The world’s largest, expanding to Miami/DC in 2026 |
| **Carrot Run** | Thousands of platforms | 17 million+ times | 22 cities (including overseas Dubai/Switzerland) | Weekly orders of 250,000+, plan to make profits in 2026 |
| **Pony.ai** | 961 units | — | Beijing/Guangzhou/Shenzhen/Shanghai | Guangzhou fleet’s bicycle revenue is balanced; listed in both Hong Kong and the United States |
| **WeRide** | ~750 units (Robotaxi) | — | Guangzhou/Nanjing/Abu Dhabi (Uber cooperation) | Abu Dhabi bicycles break even; listed in both Hong Kong and the United States |
| **Tesla** | Under testing | — | Austin, Texas (planned) | FSD pure visual route, opening in 2025.6 |

### 3.2 Chip and computing architecture

| Enterprise | Chip Platform | Computing Power | Sensor Solution | Generation |
|------|----------|------|-----------|------|
| **Waymo** (Gen6) | Self-developed + customized ASIC | — | 13 cameras + 4 lidars + 6 millimeter wave radars | Sixth generation |
| **Carrot Run** RT6 | Dual Orin-X | 508 TOPS | 8 lidars + 38 sensors (RT6) | Sixth generation |
| **Pony.ai** Gen7 | 4× Orin-X | **1016 TOPS** | 9 LiDAR + 14 cameras | 7th generation |
| **WeRide** GXR | Dual Thor (HPC 3.0) | **2000 TOPS** | Lidar (bumper type) + camera + radar | GEN8 |
| **Tesla** FSD | Self-developed FSD chip | ~144 TOPS | **Pure Vision** (8 cameras, 0 lidar) | HW4/HW5 |

### 3.3 Robotaxi system architecture



```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         Robotaxi 系统架构 (L4)                                │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌── 传感器层 ───────────────────────────────────────────────────────────┐  │
│  │                                                                       │  │
│  │  激光雷达 ×4-9                  摄像头 ×8-14                          │  │
│  │  (固态/半固态, 200m+)           (800万像素, 360°环视)                 │  │
│  │                                                                       │  │
│  │  毫米波雷达 ×4-6                超声波 ×12                            │  │
│  │  (4D 成像雷达)                  (近距泊车)                            │  │
│  │                                                                       │  │
│  │  高精定位: RTK-GNSS + IMU + 轮速 + 视觉定位                          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│         │                                                                    │
│         ▼                                                                    │
│  ┌── 计算平台层 (域控制器) ───────────────────────────────────────────────┐  │
│  │                                                                       │  │
│  │  ┌── 主计算单元 ──────────────────────────────────────────────────┐  │  │
│  │  │  SoC: 4×Orin-X (1016T) / 2×Thor (2000T) / 自研芯片            │  │  │
│  │  │  OS: Linux (实时补丁)                                          │  │  │
│  │  │                                                                │  │  │
│  │  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐    │  │  │
│  │  │  │感知    │ │预测    │ │规划    │ │控制    │ │定位    │    │  │  │
│  │  │  │        │ │        │ │        │ │        │ │        │    │  │  │
│  │  │  │BEV融合 │→│轨迹预测│→│行为决策│→│横纵向  │ │多源融合│    │  │  │
│  │  │  │3D检测  │ │意图识别│ │路径规划│ │PID/MPC│ │SLAM   │    │  │  │
│  │  │  │语义分割│ │        │ │        │ │        │ │        │    │  │  │
│  │  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘    │  │  │
│  │  └────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                       │  │
│  │  ┌── 冗余安全单元 ────────────────────────────────────────────────┐  │  │
│  │  │  Safety MCU (ASIL-D): 独立感知→独立决策→紧急制动                │  │  │
│  │  │  冗余电源 / 冗余通信 / 冗余转向 / 冗余制动                      │  │  │
│  │  └────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│         │                                                                    │
│         ▼                                                                    │
│  ┌── 线控底盘层 ─────────────────────────────────────────────────────────┐  │
│  │  线控转向 (EPS/SBW) — 冗余                                           │  │
│  │  线控制动 (EMB/EHB) — 冗余                                           │  │
│  │  线控驱动 (电机控制器)                                                │  │
│  │  线控换挡 (电子换挡)                                                  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│         │                                                                    │
│         ▼                                                                    │
│  ┌── 云端 + 远程 ────────────────────────────────────────────────────────┐  │
│  │  远程监控中心 (Teleop): 1人监管 N台车                                 │  │
│  │  高精地图更新 / 仿真平台 / 数据闭环训练                               │  │
│  │  车队管理: 调度/充电/运维/合规                                        │  │
│  │  5G + V2X 低延迟通信                                                  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```



### 3.4 Comparison of technical routes

| Route | Representation | Perception Solution | Advantages | Disadvantages |
|------|------|---------|------|------|
| **Multi-sensor fusion** | Waymo/Pony/Wenyuan/Luobo | LiDAR + camera + radar | High sensing redundancy, robust to severe weather | High cost (LiDAR accounts for 30%+) |
| **Pure Vision** | Tesla FSD | Camera only | Extremely low cost, large amount of data, fast scale | Insufficient perception of extreme scenes, safety needs to be verified |
| **Vision-based + lightweight laser** | Neolithic/White Rhinoceros (delivery) | Camera-based + 1 lidar | Moderate cost, taking into account both safety and economy | Limited sensing range (acceptable at low speed) |

### 3.5 Robotaxi cost reduction path



```
小马智行第七代系统降本:

传感器套件总成本:
  Gen6 → Gen7: 降低 70%
  其中:
    计算单元: 降低 80%
    激光雷达: 降低 68%

整车成本:
  2020年: ~100万/台 (改装+传感器)
  2023年: ~50万/台
  2025年: ~20-30万/台 (前装量产)
  目标:   ~15万/台 (规模化后)

关键降本手段:
├── 前装量产替代后装改装 (下线节拍: 1小时→10分钟)
├── 固态激光雷达替代机械式 (单颗成本: 数万→数千元)
├── SoC 集成度提升 (4颗Orin→2颗Thor, 减少板卡)
├── 零部件车规化复用 (共享乘用车供应链)
└── 算法效率提升 (减少算力需求, 减少传感器数量)
```



## 4. Panoramic comparison of chip platforms

| Chip | Manufacturer | Computing power | Technology | Main customers (unmanned vehicle field) | Positioning |
|------|------|------|------|-------|------|
| **Orin-X** | NVIDIA | 254 TOPS | 7nm | Neolithic/White Rhino/Pony.ai/Carrot Run | L4 mainstream choice |
| **Thor** | NVIDIA | 2000 TOPS | 5nm | WeRide GXR | Next generation flagship |
| **Journey 6M** | Horizon | ~100 TOPS | — | Xingshen Intelligence/Youjia Innovation | Domestic cost-effectiveness |
| **Journey 6H/P** | Horizon | 200+ TOPS | — | — | Domestic high-end |
| **FSD** | Tesla | 144 TOPS | 7nm | Tesla’s own use | Purely for visual use |
| **EyeQ6** | Mobileye | — | 7nm | — | ADAS→L4 |
| **Wu-Tang C1296** | Black Sesame | — | 7nm | — | Mid-range L4 |

## 5. Future trends

### 5.1 Unmanned delivery vehicle

| Trends | Description |
|------|------|
| **Extreme cost reduction** | The price of naked bicycles will continue to drop to less than 10,000, close to the cost of electric bicycles |
| **Pure visualization** | Evolution from "lidar + camera" to "pure vision + a small amount of ultrasound" |
| **Scenario Expansion** | Distribution → Cleaning → Security → Retail → Agriculture, multiple scenes reuse the same chassis |
| **Outbreak at sea** | Neolithic/nine consciousnesses have entered the Middle East/Southeast Asia/Japan and South Korea/Europe |
| **Standardization** | The national standard "General Technical Requirements for Unmanned Delivery Vehicles" is in progress |
| **Chip localization** | Switch from Orin to Horizon Journey 6 to reduce costs and supply chain risks |

### 5.2 Robotaxi

| Trends | Description |
|------|------|
| **Front-mounted mass production** | Rear-mounted modification→Car companies jointly front-mounted (Pony + Toyota/GAC, Wenyuan + Geely Yuan) |
| **Bicycle Profit** | Pony Guangzhou/Wenyuan Abu Dhabi has achieved balance in bicycle revenue, the industry turning point in 2026 |
| **Thor replacement** | Orin→Thor, the computing power of a bicycle is doubled, the number of boards is halved, and the cost is reduced |
| **End-to-end** | Evolution from modularity (perception → prediction → planning) to end-to-end large model |
| **Regulatory Breakthrough** | China's first batch of L3 car companies approved; Waymo highway service to open in 2026 |
| **Going overseas** | Carrot Run Dubai/Switzerland; WeRide Abu Dhabi (Uber Cooperation) |
| **Trillion Market** | The Chinese market is expected to be US$8.655 billion in 2033, with a CAGR of 74% |

### 5.3 Integration trend of the two tracks



```
当前状态:
  无人配送车: L4低速 → 独立赛道，芯片/底盘/场景完全不同于乘用车
  Robotaxi:  L4高速 → 依赖乘用车平台改装/前装

未来趋势:
  ├── 技术下溢: Robotaxi 的端到端算法 → 降维用于配送车，提升泛化能力
  ├── 芯片统一: 征程6/Orin 同时覆盖配送车和乘用车智驾
  ├── 底盘标准化: 线控底盘平台化，配送/载人/清洁共享
  └── 云端复用: 远程监控/调度/仿真/数据闭环 → 一套系统管两种车队
```



---

## Data source

- [Unmanned delivery "explodes": capital bets wildly — automotiveworld](https://www.automotiveworld.cn/zh-cn/_6/_0/2025/7/48.html)
- [Unmanned delivery, the peripheral revolution of China’s logistics — 36kr](https://36kr.com/p/3175683944632452)
- [Unmanned delivery vehicles attract 3.5 billion in revenue in half a year — Tencent News](https://news.qq.com/rain/a/20250928A088LC00)
- [More than 100 cities have opened their right of way, and autonomous vehicle delivery is about to explode — Securities Times](https://www.stcn.com/article/detail/3050000.html)
- [Global unmanned delivery vehicle market size in 2026 — Zhihu](https://zhuanlan.zhihu.com/p/2002638003785442635)
- [80% cost reduction in 3 years, dawn of functional autonomous vehicles in China - 21 Economy](https://www.21jingji.com/article/20251224/herald/7d563d21387658d76383870e01d5342a.html)
- [Robin Li: The world's number one radish race - qubit](https://www.qbitai.com/2025/11/352187.html)
- [Robotaxi’s 2025: Tesla enters the game — OFweek](https://nev.ofweek.com/2025-12/ART-77015-8400-30677159.html)
- [Pony.ai’s seventh-generation Robotaxi cost reduced by 70% — Sina Technology](https://finance.sina.com.cn/tech/csj/2025-04-24/doc-ineufhci3234483.shtml)
- [Pony.ai Domain Controller is based on Orin - Netcom](http://auto.news18a.com/news/storys_162781.html)
- [WeRide GXR powered by Thor is launched in global mass production - Electronic Engineering Special](https://www.eet-china.com/mp/a419018.html)
- [Neolithic L4 level leader in autonomous vehicles—China Automotive Technology](https://www.castc.net/news/11158.cshtml)
- [Full-level coverage of the Horizon Journey 6 series — Smart Car Resource Network](https://www.smartautoclub.com/p/108886/)
