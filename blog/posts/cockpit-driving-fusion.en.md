> Covers architecture evolution, chip platform, software layering, security isolation, and mass production implementation (as of mid-2026)

## 1. Why is it necessary to integrate the cabin and the driver?



```
传统分离架构 (2020–2024)                  舱驾一体架构 (2025–)
┌───────────┐  ┌───────────┐            ┌─────────────────────────┐
│ 座舱域控   │  │ 智驾域控   │            │ 舱驾一体中央计算平台     │
│ (8155/8295)│  │ (Orin-X)  │            │ (8775 / Thor / 星空)    │
│ Android    │  │ Linux/QNX │            │ Android + QNX + Linux   │
│ 座舱 SoC   │  │ 智驾 SoC  │            │ 单芯片 / 单板           │
└─────┬──┬──┘  └──┬──┬─────┘            └──────────┬──────────────┘
      │  │        │  │                              │
   以太网/CAN 互联                          内部总线直连
```



| Dimensions | Separated architecture | Cabin and driver integration |
|------|---------|---------|
| BOM cost | Two sets of SoC + PCB + heat dissipation + wiring harness | Single board cost reduction **20-30%** |
| Computing power utilization rate | <30% (exclusive for each domain) | **>70%** (dynamic sharing) |
| Cross-domain delay | Millisecond level (Ethernet/CAN) | **Microsecond level** (on-chip bus) |
| Data fusion | Cockpit/intelligent driving data needs to be transmitted across domains | Direct access to shared memory |
| Supply chain | Two suppliers, two integrations | One system, one integration |
| Target vehicle price range | Independent configuration for each price range | Mainly targeting **100,000-200,000** mainstream market |

## 2. Architecture evolution path



```
时间 →
2020          2022          2024          2025          2027+
  │             │             │             │             │
  ▼             ▼             ▼             ▼             ▼
分布式         域集中         跨域融合       舱驾一体       中央计算
(多ECU)       (域控制器)     (One Board)   (One Chip)    (Vehicle Computer)

┌─────┐     ┌─────┐       ┌──────────┐   ┌──────────┐  ┌──────────┐
│ECU 1│     │座舱域│       │座舱SoC   │   │          │  │          │
│ECU 2│     │控制器│       │ +        │   │ 单芯片   │  │ 中央     │
│ECU 3│     │     │       │智驾SoC   │   │ 舱驾一体 │  │ 计算机   │
│ECU 4│     │智驾域│       │ (单板)   │   │          │  │ 全域融合 │
│... │     │控制器│       └──────────┘   └──────────┘  └──────────┘
└─────┘     └─────┘
```



### Comparison of three integration forms

| Form | Description | Representative plan | Status |
|------|------|---------|------|
| **Multi Board** (multi-board multi-core) | One board each for cockpit and smart driving, Ethernet interconnection | NIO ADAM (8295 + 4×Orin-X) | Already in mass production |
| **One Board** (single board with multiple cores) | One PCB to put the cockpit + smart driving SoC, PCIe interconnection | Yikatong "single board dual core" (Longying + Orin) | Mass production in 2024 |
| **One Chip** (single chip) | A single SoC runs cockpit + smart driving at the same time | Qualcomm 8775 / NVIDIA Thor | Mass production in 2025 |

## 3. Chip platform comparison

### 3.1 List of mainstream chips

| Chip | Manufacturer | Process | AI computing power | GPU | CPU | Positioning | Mass production time |
|------|------|------|--------|-----|-----|------|---------|
| **SA8775P** | Qualcomm | 5nm | 60 TOPS | Adreno 740 | 8-core Kryo | Cabin and driver integration (mainstream) | 2025Q4 |
| **SA8797P** | Qualcomm | 3nm | ~100 TOPS | — | — | Cabin-driving integration (high-end) | 2026H2 |
| **DRIVE Thor** | NVIDIA | 5nm | 2000 TOPS | Blackwell | 12-core ARM | Cabin-Driver Integrated (Flagship) | 2025H2 |
| **Starry** | Horizon | 5nm | — | — | — | Four-domain integration (domestic) | 2026 |
| **Wudang C1296** | Black Sesame | 7nm | — | — | — | Mid-range cabin and driver integration | 2025 |
| **Dragon Eagle One** | Core Technology | 7nm | 8 TOPS | — | — | Integrated cabin and berthing (economical) | Already in mass production |

### 3.2 Three major camp routes



```
┌─────────────────────────────────────────────────────────────────────────┐
│                        舱驾一体芯片三大阵营                              │
├─────────────────────┬───────────────────────┬───────────────────────────┤
│                     │                       │                           │
│  高通阵营            │  英伟达阵营            │  国产阵营                  │
│  (跨域协同)          │  (大算力)              │  (性价比)                  │
│                     │                       │                           │
│  8295 → 8775 → 8797│  Orin → Thor          │  龍鹰一号 (芯擎)           │
│                     │                       │  星空 Starry (地平线)      │
│  主攻: 10-25万       │  主攻: 25万+旗舰      │  武当 C1296 (黑芝麻)       │
│  份额: ~70%+        │  份额: ~15%           │  X10 (芯驰)               │
│                     │                       │  A8880 (紫光展锐)          │
│  纯座舱: QNX+Android│  绑定: Linux+Android   │                           │
│  舱驾一体:          │  +QNX(安全域)          │                           │
│  QNX+Android+Linux  │                       │                           │
│  客户: 奇瑞/北汽/   │  客户: 极氪/蔚来/     │  客户: 吉利/奇瑞/         │
│        别克/日产     │        奔驰/理想       │        比亚迪/长安          │
│                     │                       │                           │
│  德赛西威/车联天下   │  德赛西威/知行科技     │  亿咖通/经纬恒润           │
│  (Tier1)            │  (Tier1)              │  (Tier1)                  │
└─────────────────────┴───────────────────────┴───────────────────────────┘
```



## 4. Software architecture design

### 4.1 Overview of layered architecture



```
┌─────────────────────────────────────────────────────────────────────────┐
│                           应用层 (Applications)                         │
│                                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │ 导航/音乐 │  │ 语音助手  │  │ 仪表渲染  │  │ ADAS HMI │               │
│  │ 视频/应用 │  │ 车控面板  │  │ (安全域)  │  │ 驾驶视图 │               │
│  │ (Android)│  │ (Android)│  │ (QNX)    │  │ (Linux)  │               │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘               │
├─────────────────────────────────────────────────────────────────────────┤
│                         中间件层 (Middleware / SOA)                      │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  SOA 服务框架 (SOME/IP + DDS)                                     │  │
│  │  ├── 跨域服务发现与通信                                            │  │
│  │  ├── 共享内存数据通道 (座舱↔智驾 零拷贝)                            │  │
│  │  ├── 传感器数据分发 (摄像头/雷达 → 智驾感知 + 座舱环视)             │  │
│  │  └── 生命周期管理 / 服务降级策略                                    │  │
│  └──────────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│                         操作系统层 (Guest OS)                            │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │ Android (VM1) │  │ QNX (VM2)    │  │ Linux (VM3)  │                 │
│  │               │  │              │  │              │                 │
│  │ 座舱娱乐      │  │ 仪表+车控    │  │ 智驾感知/    │                 │
│  │ 交互/生态     │  │ 功能安全     │  │ 规划/控制    │                 │
│  │               │  │ ASIL-D       │  │              │                 │
│  │ VIRTIO 驱动   │  │ 原生驱动     │  │ VIRTIO 驱动  │                 │
│  └───────┬───────┘  └───────┬──────┘  └───────┬──────┘                 │
│          │                  │                  │                        │
├──────────┼──────────────────┼──────────────────┼────────────────────────┤
│          ▼                  ▼                  ▼                        │
│                    Hypervisor (Type-1)                                   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  QNX Hypervisor / 鸿蒙微内核 / ACRN / Xen                        │  │
│  │  ├── CPU 核分配: 座舱4核 / 智驾4核 / 安全1核                       │  │
│  │  ├── 内存隔离: 各 VM 独立地址空间，MMU 硬件隔离                     │  │
│  │  ├── GPU/NPU 分区: 硬件级 partition 或时分复用                      │  │
│  │  ├── 中断路由: 直通 (passthrough) 或虚拟化                          │  │
│  │  └── 看门狗: 独立监控各 VM 健康状态                                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│                         硬件层 (SoC + 外设)                              │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  CPU Cluster    GPU    NPU/DSP    ISP    Video Codec    PCIe     │  │
│  │  (8-12核 ARM)   (渲染)  (AI推理)  (摄像头) (编解码)    (扩展)    │  │
│  │                                                                   │  │
│  │  DDR (LPDDR5)   eMMC/UFS   Ethernet   CAN-FD   USB   I2C/SPI   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```



### 4.2 Core role of Hypervisor



```
                     Hypervisor 资源分配示例 (8775)
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  CPU (8核 Kryo)           GPU (Adreno 740)     NPU (60 TOPS)       │
│  ┌───┬───┬───┬───┐       ┌─────────────┐      ┌──────────────┐    │
│  │C0 │C1 │C2 │C3 │       │ 40% 座舱渲染 │      │ 80% 智驾推理 │    │
│  │   Android    │       │ 30% 仪表渲染 │      │ 10% 座舱 AI  │    │
│  ├───┼───┼───┼───┤       │ 30% 智驾可视 │      │ 10% 预留     │    │
│  │C4 │C5 │C6 │C7 │       └─────────────┘      └──────────────┘    │
│  │   Linux(智驾)│                                                   │
│  │ + QNX(安全) │       内存 (16GB LPDDR5)                          │
│  └───┴───┴───┴───┘       ┌──────────────────────┐                  │
│                           │ 6GB Android          │                  │
│                           │ 4GB Linux (智驾)     │                  │
│                           │ 2GB QNX (仪表+安全)  │                  │
│                           │ 2GB Hypervisor+共享  │                  │
│                           │ 2GB GPU 显存         │                  │
│                           └──────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
```



### 4.3 Responsibilities of each Guest OS

| Guest OS | Functional safety level | Real-time | Responsibilities | Typical services |
|----------|------------|--------|------|---------|
| **QNX** | ASIL-D | Hard real-time (<1ms) | Instrument/vehicle control/security gateway | Instrument rendering, body control, safety watchdog, OTA security verification |
| **Android** | QM (no security level) | Non-real-time | Cockpit entertainment/interaction | Navigation, music, voice, app store, CarPlay/HiCar |
| **Linux** | ASIL-B (optional) | Soft real-time (<10ms) | Intelligent driving perception/planning/control | Camera ISP, obstacle detection, path planning, horizontal and vertical control |

### 4.4 Safety isolation design



```
┌─────────────────────────────────────────────────────────────────┐
│                    安全隔离三道防线                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  第一道: 硬件隔离 (SoC 级)                                       │
│  ├── ARM TrustZone: 安全世界 / 非安全世界                        │
│  ├── SMMU/MMU: 各 VM 独立地址空间，越界访问触发异常                │
│  ├── 中断隔离: 各 VM 独占中断控制器分区                           │
│  └── GPU/NPU Partition: 硬件级计算资源分区 (Orin/Thor 支持)      │
│                                                                 │
│  第二道: Hypervisor 隔离 (虚拟化层)                               │
│  ├── vCPU 绑核: QNX 绑定 safety 核，Android 绑定 perf 核         │
│  ├── 内存配额: 各 VM 内存上限硬隔离，防止 OOM 互影响             │
│  ├── I/O Passthrough: 安全关键外设直通 QNX，非安全设备走 VIRTIO   │
│  └── Watchdog: Hypervisor 监控各 VM 心跳，超时强制重启            │
│                                                                 │
│  第三道: OS 内部隔离 (操作系统层)                                  │
│  ├── QNX 微内核: 驱动/服务运行在用户态，崩溃不影响内核            │
│  ├── Android SELinux: MAC 强制访问控制                            │
│  ├── Linux seccomp + cgroup: 进程沙箱 + 资源限制                  │
│  └── 跨域通信审计: SOA 消息经 Hypervisor 代理，防止非授权访问     │
│                                                                 │
│  核心保证:                                                       │
│  ★ Android 崩溃 → 仪表(QNX)不受影响，智驾(Linux)不受影响        │
│  ★ 智驾故障 → QNX 接管最小风险状态(MRM)，座舱显示接管提示        │
│  ★ OTA 升级 → 仅更新目标 VM，其他 VM 在线不中断                  │
└─────────────────────────────────────────────────────────────────┘
```



### 4.5 Cross-domain data fusion

One of the core values of cabin-driving integration is that cross-domain data can be shared with zero copy:



```
┌── Linux (智驾) ───────────────────────┐     ┌── Android (座舱) ──────────┐
│                                       │     │                            │
│  摄像头 ISP → 感知模型推理            │     │  环视拼接渲染 (AVM)         │
│       │                               │     │       ▲                    │
│       │ 同一帧图像数据                 │     │       │                    │
│       └───────── 共享内存 ────────────┼─────┼───────┘                    │
│                  (零拷贝)             │     │                            │
│  障碍物检测结果                        │     │  HMI 显示障碍物标注        │
│       │                               │     │       ▲                    │
│       └───────── SOA 消息 ────────────┼─────┼───────┘                    │
│                  (SOME/IP)            │     │                            │
│  规划路径点                            │     │  导航叠加规划路线          │
│       └───────── SOA 消息 ────────────┼─────┼───────→                    │
│                                       │     │                            │
└───────────────────────────────────────┘     └────────────────────────────┘

对比分离架构:
  分离: 摄像头数据 → 智驾域控(处理) → 以太网(传输) → 座舱域控(再处理) → 显示
        延迟: ~20-50ms，带宽受限

  一体: 摄像头数据 → NPU(推理) + GPU(渲染) 共享同一块物理内存
        延迟: <1ms，零拷贝
```



## 5. Mass production implementation status

### 5.1 Mass-produced/designated models and smart driving functions

| Chip platform | Tier1/solution provider | Mass production model | Price | Status |
|---------|-------------|---------|------|------|
| **Qualcomm 8775** | Zhuoyu Technology | Jifox Alpha T5 | 109,800-150,000 | 2025.10 mass production |
| **Qualcomm 8775** | Desay SV | Chery integrated cabin and driving platform | 150,000-200,000 | 2025Q4 mass production |
| **Qualcomm 8775** | Momenta | Dongfeng Nissan N6 | 110,000-140,000 | 2025 mass production |
| **Qualcomm 8775** | Momenta | Buick Zhijing L7 | 170,000-220,000 | 2025 mass production |
| **NVIDIA Thor** | Desay SV IPU14 | GAC Haopin L3/L4 model | 300,000+ | 2025H2 mass production |
| **NVIDIA Thor-U** | — | Krypton 7X (2026 model) | 219,800+ | 2025.10 mass production |
| **NVIDIA Dual Thor** | — | Krypton 9X | 300,000+ | 2026 mass production |
| **Qualcomm 8797** | Lideal self-developed Mach M100 | Lideal L9 Livis | 489,800-509,800 | Mass production in 2026.5 |
| **Longying No.1** | Yikatong | Geely Galaxy E5/Lynk & Co Z20 | 100,000-150,000 | Already in mass production |
| **Wudang C1296** | — | Multiple designated locations | 100,000-200,000 | Mass production in 2025 |
| **Horizon Starry Sky** | — | Fixed point | — | 2026 |

### 5.2 Details of the intelligent driving functions implemented by each solution

#### JiFox Alpha T5 (Qualcomm 8775 + Zhuoyu Technology) — **L2+ level**

The world's first single-chip cabin-driving integrated mass production solution. 8775 single chip 72 TOPS dense computing power simultaneously runs cockpit + smart driving.

| Function category | Specific functions |
|---------|---------|
| **Urban NOA** | End-to-end urban navigation assistance without pictures (only within 150,000) |
| **High-speed NOA** | High-speed pilot assisted driving, automatic overtaking, ramp entry and exit |
| **Smart Parking** | APA automatic parking, cross-floor memory parking |
| **Active Safety** | 18 items (AEB/FCW/LDW/LKA/BSD, etc.), C-NCAP five stars |
| **Perception Hardware** | Zhuoyu Inertial Navigation Binocular Stereo Vision + 15 Radars + 7 Cameras |

#### Chery Falcon Smart Driving 500 (Qualcomm 8775) — **L2+ level**

| Function category | Specific functions |
|---------|---------|
| **High-speed NOA** | High-speed pilot assisted driving |
| **City Memory Navigation** | City navigation based on memory routes |
| **Smart Parking** | Memory parking, APA automatic parking |
| **Perception Hardware** | 8-megapixel front-view camera + ultrasonic radar, 80-128 TOPS |

#### Dongfeng Nissan N6 (Qualcomm 8775 + Momenta) — **L2+ level**

| Function category | Specific functions |
|---------|---------|
| **City NOA** | Momenta City Navigation Assistance |
| **High-speed NOA** | High-speed pilot assist |
| **Smart Parking** | Full-scenario intelligent assisted parking |
| **Cockpit AI** | iFlytek Spark + DeepSeek large model |

#### Buick Zhijing L7 (Qualcomm 8775 cockpit + Momenta R6 smart driving) — **L2+ level**

Note: The 8775 of Zhijing L7 is mainly responsible for the cockpit, and the smart driving is carried by the independent Momenta solution, which belongs to the "8775 for cockpit + smart driving independent" mode.

| Function category | Specific functions |
|---------|---------|
| **City NOA** | No breakpoint city NOA (Momenta R6 reinforcement learning large model) |
| **Smart Parking** | One-click parking without parking |
| **Cockpit** | 8775 drives 8-screen linkage |

#### Extreme Krypton 7X 2026 model (NVIDIA Thor-U 700TOPS) — **L2++ level**

| Function category | Specific functions |
|---------|---------|
| **D2D Navigation** | Full navigation assistance from parking space to parking space (D2D) |
| **City NOA** | NZP City Navigation Assistance (Smart Driving without Map) |
| **High-speed NOA** | High-speed autonomous piloting, automatic overtaking, and tunnel following |
| **Smart Parking** | APA/RAPA remote control parking/HPA memory parking, etc. 15+ items |
| **Perception Hardware** | 1 lidar (standard for all series), Qianlihaohan H7 system |
| **Covered scenes** | 30+ driving scenes: traffic light recognition, unprotected left turns, etc. |

#### JiKrypton 9X (NVIDIA dual Thor + 5 lidar) - **Close to L3 level**

| Function category | Specific functions |
|---------|---------|
| **City NOA** | Close to L3 city NOA |
| **Park Roaming** | Unpictured Park Roaming + Dynamic Semantic Understanding |
| **Perception Hardware** | Dual Thor chips + 5 lidar + 43 sensing hardware, fully redundant architecture |

#### GAC Haopin (NVIDIA Thor / Desay SV IPU14) - **L3/L4 level**

| Function category | Specific functions |
|---------|---------|
| **Urban NOA** | Standard for all series, urban scene coverage >99% |
| **L3 admission** | The first batch of national car companies admitted to L3 autonomous driving |
| **L4 Operation** | L4 autonomous driving cumulative operation exceeds 40 million kilometers |
| **Smart Driving Model** | VLA visual language model + world model (G1000 solution) |

#### Ideal L9 Livis (Qualcomm 8797 + self-developed Mach M100×2) — **L2++ level**

| Function category | Specific functions |
|---------|---------|
| **Full-scenario NOA** | High-speed + urban full-scenario navigation assistance |
| **Smart Parking** | Full-scenario smart parking |
| **Smart Driving Chip** | Dual Mach M100, total computing power 2560 TOPS |
| **Smart Driving Model** | Mach VLA large visual language model, reducing end-to-end latency by 40% |
| **Perception Hardware** | 4 solid-state LiDAR + 8-megapixel camera matrix + 11 cameras + 10 UWB |

#### Geely Galaxy E5 (Xinqing Longying No. 1 8 TOPS) — **L2 level**

| Function category | Specific functions |
|---------|---------|
| **L2 ADAS** | ACC/LKA/AEB and other basic assisted driving |
| **Automatic Parking** | APA Automated Parking |
| **Cockpit** | Mainstream smart cockpit functions |
| **Positioning** | Cabin and berth all in one (One Chip, ultimate cost-effectiveness, 100,000 level) |

### 5.3 Summary of smart driving function levels



```
                        智驾能力 →
       L2 基础        L2+ 高速NOA      L2++ 城市NOA      L3 脱手脱眼     L4 无人驾驶
        │                │                 │                │               │
  ┌─────┴──────┐   ┌─────┴──────┐   ┌─────┴──────┐   ┌────┴─────┐   ┌────┴─────┐
  │银河E5      │   │奇瑞猎鹰500 │   │极狐T5      │   │广汽昊铂  │   │广汽昊铂  │
  │(龍鹰 8T)   │   │(8775 128T) │   │(8775 72T)  │   │(Thor)    │   │(IPU14)   │
  │            │   │            │   │东风日产N6   │   │          │   │(限定场景)│
  │            │   │            │   │别克至境L7   │   │极氪9X    │   │          │
  │            │   │            │   │            │   │(双Thor)  │   │          │
  │            │   │            │   │极氪7X      │   │          │   │          │
  │            │   │            │   │(Thor 700T) │   │          │   │          │
  │            │   │            │   │理想L9      │   │          │   │          │
  │            │   │            │   │(马赫2560T) │   │          │   │          │
  └────────────┘   └────────────┘   └────────────┘   └──────────┘   └──────────┘
  ~8 TOPS           80-128 TOPS      72-2560 TOPS     700+ TOPS      2000+ TOPS
  10万以下           10-15万          11-50万           30万+           30万+
```



### 5.2 Desai West Wido Route Layout



```
德赛西威舱驾一体产品矩阵:

高端旗舰:
  IPU14 (Thor-U, 2000 TOPS)
  └── 单芯片舱驾控一体, L3+L4, 广汽昊铂

中高端:
  ICP Aurora (多芯方案)
  └── Orin + 8295 + 黑芝麻A1000, 已量产

主流:
  8775 舱驾一体平台
  └── 单芯片, 奇瑞/塔塔, 降本20-30%

下一代:
  8797 平台
  └── 与高通/卓驭科技联合开发, 2026+

适配芯片: SA8620P / QAM8650P / QAM8775P / Thor-U
```



## 6. Challenges faced

| Challenge | Description | Solutions |
|------|------|---------|
| **Functional Safety Certification** | Running entertainment + security domain on a single chip, fault isolation needs to be proven | QNX ASIL-D + Hypervisor hardware isolation certification |
| **Computing power allocation** | Intelligent driving requires sudden computing power (emergency obstacle avoidance), and the cockpit also needs to be smooth | Hypervisor dynamic scheduling + QoS policy + NPU partitioning |
| **Thermal Design** | Single chip power consumption 30-80W (Thor ~60W) | Liquid cooling/vapor chamber cooling solution |
| **Supply chain dependence** | Qualcomm/NVIDIA monopoly on high-end chips | Domestic chips are accelerating to catch up (Horizon/Black Sesame/Xinqing) |
| **Software complexity** | Three OS + Hypervisor + SOA middleware | Tier1 provides turnkey solution; AUTOSAR AP standardization |
| **OTA upgrade** | Need to support independent upgrade of each VM without interrupting other domains | A/B partition + differential upgrade + Hypervisor hot switch |
| **Network Security** | Cross-domain communication increases the attack surface | Cross-domain firewall + message signature + HSM hardware security module |

## 7. Market Forecast

| Indicators | 2024 | 2025 | 2026 | 2030 |
|------|------|------|------|------|
| Cabin-driving integrated vehicle capacity (China) | 440,000 vehicles | ~1.2 million vehicles | ~3 million vehicles | — |
| Penetration rate | ~2% | ~5% | ~12% | **>30%** |
| One Chip Proportion | <5% | ~20% | ~40% | >60% |
| Qualcomm chip share | >80% | ~70% | ~65% | ~55% |
| Domestic chip share | <10% | ~15% | ~20% | ~30% |

---

## Data source

- [Integrated Cabin and Driving: Toward the Era of Single-chip Mass Production - Smart Automotive Resource Network](https://www.smartautoclub.com/p/109673/)
- [Cabin-driving integration is testing the 100,000 level, and the penetration rate will exceed 30% in 2030 - CSDN/High Engineering Intelligence](https://blog.csdn.net/GGAI_AI/article/details/154476352)
- [Application differences between Qualcomm Snapdragon SA8775P and SA8295P — EDN](https://www.ednchina.com/technews/36418.html)
- [Qualcomm, Horizon, and Black Sesame compete for cabin-driving integration — Tencent News](https://news.qq.com/rain/a/20260326A0725N00)
- [Qualcomm launches the world's first central computing solution - Qubits](https://www.qbitai.com/2025/07/303775.html)
- [The impact of the One board/One Chip solution on the automotive supply chain — Zuosi Auto Research](https://zhuanlan.zhihu.com/p/14860131488)
- [Cockpit Domain Controller: Three Architectures for AI — Zhihu](https://zhuanlan.zhihu.com/p/1922969345174255365)
- [BlackBerry QNX: Cabin-driving integration brings new opportunities — 36kr](https://36kr.com/p/2044716025580549)
- [QNX Advanced Virtualization Framework — CSDN](https://blog.csdn.net/qrx941017/article/details/145420182)
- [300 car models, US$45 billion in orders: Qualcomm’s automotive chip’s Chinese chess game - NetEase](https://www.163.com/dy/article/KUO0DVC405118O8G.html)
