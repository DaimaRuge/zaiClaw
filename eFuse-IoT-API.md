# eFuse Mini - 涂鸦IoT开发API接口汇总

本文档整理了eFuse Mini智能电量统计插座对接涂鸦IoT云平台所需的全部API接口，按功能模块分类整理，方便研发对接查阅。

---

## 目录

| 模块 | 说明 |
|------|------|
| [1. 认证授权](#1-认证授权) | 获取access_token，身份认证 |
| [2. 设备管理](#2-设备管理) | 设备信息查询、列表查询、移除、改名等 |
| [3. 设备功能控制](#3-设备功能控制) | 下发控制指令（开关等） |
| [4. 设备状态数据](#4-设备状态数据) | 获取设备实时状态、电量数据 |
| [5. 设备日志](#5-设备日志) | 查询设备操作历史 |
| [6. 用户管理](#6-用户管理) | 设备关联用户管理 |
| [7. 云云对接调用流程](#7-云云对接调用流程) | 完整调用链路说明 |

---

## 1. 认证授权

### 1.1 获取访问令牌

| 请求方式 | API 端点 | 功能说明 |
|----------|----------|----------|
| GET | `/v1.0/token?grant_type=1` | **简单模式** - 云项目数据访问获取token |
| GET | `/v1.0/token?grant_type=2&code={code}` | **OAuth 2.0模式** - 用户授权数据访问获取token |

**响应示例：**
```json
{
  "result": {
    "access_token": "3f4eda2bdec17232f67c0b188af3****",
    "expire_time": 7200
  },
  "success": true
}
```

---

## 2. 设备管理

| 请求方式 | API 端点 | 功能说明 |
|----------|----------|----------|
| GET | `/v1.0/devices/{device_id}` | 获取设备详情（含最新状态） |
| GET | `/v1.0/users/{uid}/devices` | 获取指定用户下的设备列表 |
| GET | `/v1.0/devices` | 批量获取设备列表（按应用/产品/设备ID查询） |
| PUT | `/v1.0/devices/{device_id}/functions/{function_code}` | 修改功能点名称 |
| PUT | `/v1.0/devices/{device_id}/reset-factory` | 恢复设备出厂设置 |
| DELETE | `/v1.0/devices/{device_id}` | 移除设备 |
| GET | `/v1.0/devices/{deviceId}/sub-devices` | 查询网关下子设备列表 |
| GET | `/v1.0/devices/factory-infos` | 查询设备出厂信息 |
| PUT | `/v1.0/devices/{device_id}` | 修改设备名称 |

---

## 3. 设备功能控制

| 请求方式 | API 端点 | 功能说明 |
|----------|----------|----------|
| POST | `/v1.0/devices/{device_id}/commands` | 下发控制指令 |

**请求Body示例（开关控制）：**
```json
{
  "commands": [
    {
      "code": "switch_1",
      "value": true
    }
  ]
}
```

**响应示例：**
```json
{
  "result": true,
  "success": true
}
```

---

## 4. 设备状态数据

| 请求方式 | API 端点 | 功能说明 |
|----------|----------|----------|
| GET | `/v1.0/devices/{device_id}/status` | 获取设备当前所有功能点状态 |

**响应示例：**
```json
{
  "result": [
    {"code": "switch_1", "value": true},
    {"code": "cur_current", "value": 125},
    {"code": "cur_power", "value": 27},
    {"code": "cur_voltage", "value": 221},
    {"code": "add_ele", "value": 12500}
  ],
  "success": true
}
```

**数据单位换算：**

| DP标识符 | 单位 | 换算说明 |
|----------|------|----------|
| `cur_current` | mA | 实际电流 = value / 1000 A |
| `cur_power` | W | 无需换算 |
| `cur_voltage` | V | 无需换算 |
| `add_ele` | 0.001 kWh | 实际电量 = value / 1000 kWh |

---

## 5. 设备日志

| 请求方式 | API 端点 | 功能说明 |
|----------|----------|----------|
| GET | `/v1.0/devices/{device_id}/logs` | 查询设备操作历史记录 |

**请求参数：**
- `type`: 日志事件类型，多个用逗号分隔
- `start_time` / `end_time`: 13位时间戳查询范围
- `size`: 查询条数，默认20

---

## 6. 用户管理

| 请求方式 | API 端点 | 功能说明 |
|----------|----------|----------|
| POST | `/v1.0/devices/{device_id}/user` | 新增设备用户 |
| DELETE | `/v1.0/devices/{device_id}/users/{user_id}` | 删除指定用户 |
| PUT | `/v1.0/devices/{device_id}/users/{user_id}` | 修改指定用户 |
| GET | `/v1.0/devices/{device_id}/users/{user_id}` | 查询指定用户信息 |
| GET | `/v1.0/devices/{device_id}/users` | 查询设备关联的用户列表 |
| PUT | `/v1.0/devices/{device_id}/multiple-name` | 修改多路名称 |
| GET | `/v1.0/devices/{device_id}/multiple-names` | 获取多路名称 |

---

## 7. 云云对接调用流程

### 7.1 整体架构

```
┌─────────────┐
│  eFuse 设备 │
└──────┬──────┘
       │ MQTT → 涂鸦云
       ▼
┌─────────────┐
│  涂鸦IoT云  │
└──────┬──────┘
       │ HTTPS REST → 客户侧云
       ▼
┌─────────────┐
│  客户侧业务  │
└─────────────┘
```

### 7.2 调用步骤

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 获取access_token | 调用 `/v1.0/token` 获取令牌 |
| 2 | 获取设备列表 | 调用 `/v1.0/devices` 或 `/v1.0/users/{uid}/devices` |
| 3 | 查询设备状态 | 调用 `/v1.0/devices/{device_id}/status` 获取实时数据 |
| 4 | 下发控制指令 | 调用 `/v1.0/devices/{device_id}/commands` 控制开关 |
| 5 | 查询历史日志 | 调用 `/v1.0/devices/{device_id}/logs` 查询操作记录 |

### 7.3 授权方式选择

| 模式 | grant_type | 适用场景 |
|------|------------|----------|
| 简单模式 | 1 | 对接云项目下所有设备，server-to-server |
| OAuth 2.0 | 2 | 需要终端用户授权，访问授权用户数据 |

### 7.4 重要提示

- **签名要求**：所有请求必须携带 `client_id` + `sign` + `sign_method=HMAC-SHA256` + `t`（13位时间戳）
- **content-type**：POST请求必须设置 `Content-Type: application/json`
- **地域选择**：根据设备所在地选择就近接入地址，降低延迟

| 地域 | Base URL |
|------|----------|
| 中国 | `https://openapi.tuyacn.com` |
| 美西 | `https://openapi.tuyaus.com` |
| 中欧 | `https://openapi.tuyaeu.com` |

---

## 附录

### eFuse Mini 物模型DP点对照表

| DP ID | 标识符 | 方向 | 类型 | 功能说明 | 是否必选 |
|-------|----------|------|------|----------|----------|
| 1 | `switch_1` | 可下发可上报 | bool | 继电器开关 | ✅ 必选 |
| 9 | `countdown_1` | 可下发可上报 | value | 倒计时开关 | ✅ 必选 |
| 17 | `add_ele` | 可下发可上报 | value | 累计增量电量 | ✅ 必选 |
| 18 | `cur_current` | 只上报 | value | 实时电流 | ✅ 必选 |
| 19 | `cur_power` | 只上报 | value | 实时功率 | ✅ 必选 |
| 20 | `cur_voltage` | 只上报 | value | 实时电压 | ✅ 必选 |
| 21 | `test_bit` | 只上报 | value | 产测结果 | ✅ 必选 |
| 22 | `voltage_coe` | 只上报 | value | 电压校准系数 | ✅ 必选 |
| 23 | `electric_coe` | 只上报 | value | 电流校准系数 | ✅ 必选 |
| 24 | `power_coe` | 只上报 | value | 功率校准系数 | ✅ 必选 |
| 25 | `electricity_coe` | 只上报 | value | 电量校准系数 | ✅ 必选 |
| 26 | `fault` | 只上报 | fault | 故障告警 | ✅ 必选 |
| 38 | `relay_status` | 可下发可上报 | enum | 上电状态设置 | ⭕ 可选 |
| 41 | `cycle_time` | 可下发可上报 | string | 循环定时 | ⭕ 可选 |
| 42 | `random_time` | 可下发可上报 | string | 随机定时 | ⭕ 可选 |

### 故障告警码

| Bit | 故障值 | 说明 |
|-----|--------|------|
| 0 | `ov_cr` | 过流 |
| 1 | `ov_vol` | 过压 |
| 2 | `ov_pwr` | 过功率 |
| 3 | `ls_cr` | 欠流 |
| 4 | `ls_vol` | 欠压 |
| 5 | `ls_pow` | 欠功率 |

---

**文档版本**：v1.0  
**整理日期**：2026-03-25  
**适用产品**：eFuse Mini 智能电量统计插座  
**来源文档**：https://developer.tuya.com/cn/docs/iot/product-standard-function-introduction?id=K9tp15ceh63gr
