<template>
  <div class="page-container">
    <div class="simulation-container">
      <div class="left-panel">
        <div class="panel-header">
          <h2>设备类型</h2>
        </div>
        <div class="device-list">
          <div v-for="device in deviceTemplates" 
               :key="device.id"
               class="device-item"
               draggable="true"
               @dragstart="dragStart(device)">
            <div class="device-icon" :class="device.icon">
              <i :class="getDeviceIcon(device.id)"></i>
            </div>
            <div class="device-info">
              <span class="device-name">{{ device.name }}</span>
              <span class="device-desc">{{ device.description }}</span>
            </div>
            <div class="drag-handle">
              <i class="el-icon-rank"></i>
            </div>
          </div>
        </div>
      </div>

      <div class="right-panel">
        <div class="workspace-header">
          <div class="header-content">
            <h2>仿真配置区域</h2>
            <el-button 
              type="primary" 
              class="start-simulation-btn"
              @click="generateSimulation" 
              :disabled="!configuredDevices.length">
              <i class="el-icon-video-play"></i>
              开始仿真
            </el-button>
          </div>
        </div>

        <div class="workspace"
             @dragover.prevent
             @drop="onDrop"
             :class="{ 'is-empty': !configuredDevices.length }">
          
          <div v-if="!configuredDevices.length" class="empty-tip">
            <div class="empty-animation">
              <i class="el-icon-upload"></i>
            </div>
            <p>将设备拖拽到此处开始配置</p>
          </div>

          <transition-group name="device-list" tag="div" class="configured-devices">
            <div v-for="(device, index) in configuredDevices" 
                 :key="device.id"
                 class="configured-device-card"
                 :class="device.name">
              <div class="card-header">
                <div class="header-left">
                  <i :class="getDeviceIcon(device.id)"></i>
                  <span>{{ device.name }}</span>
                </div>
                <div class="header-right">
                  <span class="device-id">设备ID: {{ device.deviceId }}</span>
                  <el-button type="text" @click="removeDevice(index)" class="delete-btn">
                    <i class="el-icon-delete"></i>
                  </el-button>
                </div>
              </div>

              <el-form class="device-form" label-position="top">
                <el-row :gutter="20">
                  <el-col :span="12" v-for="field in device.fields" :key="field.code">
                    <el-form-item 
                      :label="field.name"
                      :class="{ 'is-required': isFieldRequired(field) }">
                      <el-tooltip :content="getFieldDescription(device.id, field.code)" placement="top">
                        <div class="slider-wrapper">
                          <el-slider
                            v-model="device.data[field.code]"
                            :min="getFieldMin(device.id, field.code)"
                            :max="getFieldMax(device.id, field.code)"
                            :step="getFieldStep(device.id, field.code)"
                            :format-tooltip="(val) => val + getFieldUnit(device.id, field.code)"
                            show-input>
                          </el-slider>
                        </div>
                      </el-tooltip>
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
            </div>
          </transition-group>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.simulation-container {
  display: flex;
  gap: 20px;
  padding: 20px;
  min-height: calc(100vh - 40px);
  background: #f0f2f5;
}

.left-panel {
  width: 300px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.right-panel {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.panel-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.device-list {
  padding: 10px;
}

.device-item {
  display: flex;
  align-items: center;
  padding: 15px;
  margin-bottom: 10px;
  background: #f8f9fa;
  border-radius: 6px;
  cursor: move;
  transition: all 0.3s ease;
}

.device-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.device-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  font-size: 20px;
}

.device-icon.water-meter { background: #e6f7ff; color: #1890ff; }
.device-icon.water-pipe { background: #f6ffed; color: #52c41a; }
.device-icon.water-pump { background: #fff7e6; color: #fa8c16; }

.device-info {
  flex: 1;
}

.device-name {
  display: block;
  font-weight: 500;
  margin-bottom: 4px;
}

.device-desc {
  font-size: 12px;
  color: #999;
}

.workspace {
  padding: 20px;
  min-height: 500px;
  background: #fafafa;
  border-radius: 8px;
  margin: 20px;
}

.workspace.is-empty {
  border: 2px dashed #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-tip {
  text-align: center;
  color: #999;
}

.empty-animation {
  font-size: 48px;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

.configured-device-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.configured-device-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 500;
}

.delete-btn:hover {
  color: #f56c6c;
}

.unit {
  color: #909399;
  font-size: 12px;
}

/* 动画效果 */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.device-list-enter-active, .device-list-leave-active {
  transition: all 0.5s ease;
}

.device-list-enter, .device-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* 设备卡片特定样式 */
.水表 { border-left: 4px solid #1890ff; }
.水泵 { border-left: 4px solid #52c41a; }
.水管 { border-left: 4px solid #fa8c16; }

/* 响应式局 */
@media screen and (max-width: 1200px) {
  .simulation-container {
    flex-direction: column;
  }
  
  .left-panel {
    width: 100%;
  }
}

.workspace-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.start-simulation-btn {
  background-color: #409eff;
  border: none;
  padding: 12px 24px;
  font-size: 14px;
  border-radius: 8px;
  color: white;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.start-simulation-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
  background-color: #66b1ff;
}

.start-simulation-btn:active {
  transform: translateY(0);
}

.start-simulation-btn:disabled {
  background-color: #c0c4cc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.input-with-slider {
  position: relative;
  width: 100%;
}

.slider-dialog .el-dialog__body {
  padding: 30px;
}

.slider-container {
  padding: 20px;
}

/* 自定义滑块样式 */
.el-slider__runway {
  background-color: #e4e7ed;
}

.el-slider__bar {
  background-color: #409eff;
}

.el-slider__button {
  border-color: #409eff;
}

.el-input.is-disabled .el-input__inner {
  cursor: pointer;
  background-color: #fff;
}

/* 添加防止闪烁的样式 */
.el-dialog {
  transform: none;
  margin: 0 auto !important;
}

.slider-dialog {
  position: relative;
}

.slider-container {
  padding: 20px;
  min-height: 100px;
}

/* 修复弹窗样式 */
:deep(.el-dialog__wrapper) {
  z-index: 2000 !important;
}

:deep(.v-modal) {
  z-index: 1999 !important;
}

/* 确保滑块在弹窗内正确显示 */
.slider-container {
  padding: 20px;
  background: #fff;
}

/* 确保输入框可点击 */
.input-with-slider {
  cursor: pointer;
}

.el-input__inner {
  cursor: pointer !important;
}

.slider-dialog {
  display: flex;
  flex-direction: column;
}

.slider-container {
  padding: 30px;
  min-height: 120px;
  display: flex;
  align-items: center;
}

:deep(.el-slider) {
  width: 100%;
}

:deep(.el-dialog__body) {
  padding: 0;
}

.dialog-footer {
  padding: 20px;
  text-align: right;
}

/* 确保弹窗在最上层 */
:deep(.el-dialog__wrapper) {
  z-index: 2001 !important;
}

:deep(.v-modal) {
  z-index: 2000 !important;
}

/* 输入框样式 */
.input-with-slider {
  cursor: pointer;
}

.el-input__inner {
  cursor: pointer !important;
}

/* 修改弹样式 */
:deep(.el-dialog) {
  margin-top: 15vh !important;
}

:deep(.el-dialog__body) {
  padding: 20px 30px;
}

.slider-container {
  padding: 20px 0;
}

.dialog-footer {
  text-align: right;
  padding-top: 20px;
}

/* 确保滑块在弹窗中正确显示 */
:deep(.el-slider) {
  width: 100%;
  margin: 20px 0;
}

/* 确保弹窗在最上 */
:deep(.el-dialog__wrapper) {
  z-index: 2001 !important;
}

:deep(.v-modal) {
  z-index: 2000 !important;
}

/* 添加滑块相关样式 */
.slider-wrapper {
  padding: 10px 0;
}

:deep(.el-slider) {
  width: 100%;
}

:deep(.el-slider__input) {
  width: 120px;
}

:deep(.el-slider__runway) {
  margin: 16px 0;
}

:deep(.el-tooltip__popper) {
  max-width: 200px;
}

:deep(.el-form-item) {
  margin-bottom: 25px;
}

:deep(.el-form-item__label) {
  padding-bottom: 8px;
  font-weight: 500;
}

/* 添加单位显示样式 */
:deep(.el-slider__input) .el-input__suffix {
  right: 5px;
  color: #909399;
}

/* 优化滑块交互样式 */
:deep(.el-slider__button) {
  border-color: #409EFF;
  width: 16px;
  height: 16px;
}

:deep(.el-slider__bar) {
  background-color: #409EFF;
}

:deep(.el-slider__button:hover) {
  transform: scale(1.1);
}

/* 响应式调整 */
@media screen and (max-width: 768px) {
  :deep(.el-slider__input) {
    width: 100px;
  }
  
  .el-col {
    width: 100%;
  }
}

.device-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.device-form {
  padding: 0 20px;
}

/* 调整表单项布局 */
:deep(.el-form-item) {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
}

:deep(.el-form-item__label) {
  width: 100px;
  text-align: right;
  padding-right: 20px;
  line-height: 1.5;
  font-weight: 500;
}

:deep(.el-form-item__content) {
  flex: 1;
  margin-left: 0 !important;
}

/* 滑块容器样式 */
.slider-wrapper {
  flex: 1;
  padding: 0 20px;
}

/* 滑块样式优化 */
:deep(.el-slider) {
  width: 100%;
}

:deep(.el-slider__runway) {
  flex: 0 1 calc(100% - 130px);
  display: flex;
  align-items: center;
}

:deep(.el-slider__input) {
  width: 130px;
  margin-left: 20px;
}

/* 单位显示样式 */
:deep(.el-slider__input) .el-input__suffix {
  right: 5px;
  color: #909399;
}

/* 响应式调整 */
@media screen and (max-width: 768px) {
  .device-form {
    padding: 0;
  }

  :deep(.el-form-item) {
    flex-direction: column;
    align-items: flex-start;
  }

  :deep(.el-form-item__label) {
    width: 100%;
    text-align: left;
    padding-bottom: 8px;
  }

  .slider-wrapper {
    width: 100%;
    padding: 0;
  }

  :deep(.el-slider__input) {
    width: 100px;
  }
}

.device-id {
  color: #909399;
  font-size: 14px;
  margin-right: 10px;
  font-weight: 500;
}
</style>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      deviceTemplates: [
        {
          id: 'water-meter',
          name: '水表',
          fields: [
            { name: '流量', code: 'flux', type: 'Double' },
            { name: '压力', code: 'pressure', type: 'Double' },
            { name: '信号强度', code: 'signal', type: 'INT' },
            { name: '电压', code: 'voltage', type: 'Double' },
            { name: '酸碱度', code: 'ph', type: 'Double' },
            { name: '浊度', code: 'turb', type: 'Double' },
            { name: '臭氧', code: 'ozone', type: 'Double' },
            { name: '口径', code: 'caliber', type: 'Double' }
          ]
        },
        {
          id: 'water-pipe',
          name: '水管',
          fields: [
            { name: '管段', code: 'pipe_stage', type: 'INT' },
            { name: '管龄', code: 'pipe_age', type: 'Double' },
            { name: '管径', code: 'pipe_diameter', type: 'Double' },
            { name: '管长', code: 'pipe_length', type: 'Double' },
            { name: '压力', code: 'pipe_pressure', type: 'Double' },
            { name: '流量', code: 'flux', type: 'Double' },
            { name: '埋深', code: 'bury_depth', type: 'Double' },
            { name: '口径', code: 'caliber', type: 'Double' }
          ]
        },
        {
          id: 'water-pump',
          name: '水泵',
          fields: [
            { name: '温度', code: 'temp', type: 'Double' },
            { name: '震动', code: 'shake', type: 'Number' },
            { name: '湿度', code: 'humidity', type: 'Double' },
            { name: '流量', code: 'flux', type: 'Double' },
            { name: '功率', code: 'power', type: 'INT' },
            { name: '噪音', code: 'noise', type: 'Double' },
            { name: '口径', code: 'caliber', type: 'Double' }
          ]
        }
      ],
      configuredDevices: [],
      editingDevice: null,
      // 字段单位和描述信息
      fieldInfo: {
        'water-meter': {
          flux: { unit: 'm³/h', description: '水表流量数据' },
          pressure: { unit: 'MPa', description: '水表压力数据' },
          signal: { unit: 'dBm', description: '无线信号强度' },
          voltage: { unit: 'V', description: '设备电压' },
          ph: { unit: 'pH', description: '水酸碱度' },
          turb: { unit: 'NTU', description: '水质浊度' },
          ozone: { unit: 'mg/L', description: '臭氧浓' },
          caliber: { unit: 'mm', description: '水表口径' }
        },
        'water-pipe': {
          pipe_stage: { unit: '', description: '管道段落类型' },
          pipe_age: { unit: '年', description: '管道使用年限' },
          pipe_diameter: { unit: 'mm', description: '管道直径' },
          pipe_length: { unit: 'm', description: '管道长度' },
          pipe_pressure: { unit: 'bar', description: '管道压力' },
          flux: { unit: 'm³/h', description: '管道流量' },
          bury_depth: { unit: 'm', description: '管道埋深' },
          caliber: { unit: 'mm', description: '管道口径' }
        },
        'water-pump': {
          temp: { unit: '°C', description: '水泵温度' },
          shake: { unit: 'Hz', description: '震动频率' },
          humidity: { unit: '%', description: '相对湿度' },
          flux: { unit: 'm³/h', description: '水泵流量' },
          power: { unit: 'kW', description: '运行功率' },
          noise: { unit: 'dB(A)', description: '运行噪音' },
          caliber: { unit: 'mm', description: '水泵口径' }
        }
      },
      dialogVisible: false,
      currentSlider: {
        title: '',
        value: 0,
        min: 0,
        max: 100,
        step: 1,
        unit: '',
        deviceId: '',
        fieldCode: '',
        device: null
      },
      fieldRanges: {
        'water-meter': {
          flux: { 
            min: 0.5,    // 小口径最小流量
            max: 100,    // 中口径最大流量
            step: 0.5 
          },
          pressure: { min: 0, max: 1.6, step: 0.1 },  // 标准水压范围
          signal: { min: -100, max: -40, step: 1 },   // 信号强度范围
          voltage: { min: 3.3, max: 24, step: 0.1 },  // 电压范围
          ph: { min: 6.5, max: 8.5, step: 0.1 },      // 生活用水pH范围
          turb: { min: 0, max: 5, step: 0.1 },        // 生活用水浊度范围
          ozone: { min: 0, max: 0.3, step: 0.01 },    // 臭氧范围
          caliber: { 
            min: 15,     // 小口径最小值
            max: 150,    // 中口径最大值
            step: 5 
          }
        },
        'water-pipe': {
          pipe_stage: { min: 1, max: 5, step: 1 },          // 管道阶段
          pipe_age: { min: 0, max: 50, step: 1 },           // 管道使用年限
          pipe_diameter: { 
            min: 15,     // 小口径最小值(15mm)
            max: 150,    // 中口径最大值(150mm)
            step: 5 
          },
          pipe_length: { min: 1, max: 1000, step: 1 },      // 管道长度(米)
          pipe_pressure: { min: 0.2, max: 1.6, step: 0.1 }, // 标准水压范围
          flux: { 
            min: 0.5,    // 小口径最小流量(0.5 m³/h)
            max: 100,    // 中口径最大流量(100 m³/h)
            step: 0.5 
          },
          bury_depth: { min: 0.8, max: 3, step: 0.1 },      // 标准埋深范围
          caliber: { 
            min: 15,     // 小口径最小值
            max: 150,    // 中口径最大值
            step: 5 
          }
        },
        'water-pump': {
          temp: { min: 10, max: 60, step: 0.1 },        // 温度范围
          shake: { min: 10, max: 2000, step: 10 },      // 震动范围
          humidity: { min: 20, max: 80, step: 1 },      // 湿度范围
          flux: { 
            min: 1,      // 小型泵最小流量(1 m³/h)
            max: 200,    // 中型泵最大流量(200 m³/h)
            step: 1 
          },
          power: { min: 0.5, max: 200, step: 0.5 },     // 调整为中小型泵功率范围
          noise: { min: 60, max: 90, step: 1 },         // 噪音范围
          caliber: { 
            min: 50,     // 小型泵最小口径
            max: 150,    // 中型泵最大口径
            step: 5 
          }
        }
      }
    }
  },

  methods: {
    async generateSimulation() {
      for (const device of this.configuredDevices) {
        try {
          const data = device.data
          const requestData = {
            data: {
              device_type: device.id,
              device_id: device.deviceId,
              ...data
            }
          }

          const response = await axios.post('http://localhost:8088/api/simulation/data', requestData)
          
          if(response.data) {
            this.$message.success(`${device.id.toUpperCase()}数据保存成功`)
          }
        } catch (error) {
          console.error('保存设备数据失败:', error)
          this.$message.error(`保存失败: ${error.message}`)
        }
      }
    },

    getFieldUnit(deviceId, fieldCode) {
      return this.fieldInfo[deviceId]?.[fieldCode]?.unit || ''
    },

    getFieldDescription(deviceId, fieldCode) {
      return this.fieldInfo[deviceId]?.[fieldCode]?.description || ''
    },

    dragStart(device) {
      event.dataTransfer.setData('deviceType', device.id)
    },

    onDrop(event) {
      const deviceType = event.dataTransfer.getData('deviceType')
      const template = this.deviceTemplates.find(t => t.id === deviceType)
      
      if (template) {
        this.configuredDevices.push({
          id: template.id,
          deviceId: this.generateRandomId(template.id),
          name: template.name,
          fields: template.fields,
          data: {}
        })
        
        this.$message.success(`已添加${template.name}配置`)
      }
    },

    removeDevice(index) {
      this.configuredDevices.splice(index, 1)
    },

    getDeviceIcon(deviceId) {
      const icons = {
        'water-meter': 'el-icon-odometer',
        'water-pipe': 'el-icon-connection',
        'water-pump': 'el-icon-refresh'
      }
      return icons[deviceId]
    },

    isFieldRequired(field) {
      // 可以根据业务需求设置必填字段
      return true
    },

    getFieldPlaceholder(deviceId, fieldCode) {
      return `请输入${this.fieldInfo[deviceId][fieldCode].description}`
    },

    showSlider(device, field) {
      console.log('showSlider called', device, field);
      this.currentSlider = {
        title: field.name + '设置',
        value: device.data?.[field.code] || 0,
        min: this.getFieldMin(device.id, field.code),
        max: this.getFieldMax(device.id, field.code),
        step: this.getFieldStep(device.id, field.code),
        unit: this.getFieldUnit(device.id, field.code),
        deviceId: device.id,
        fieldCode: field.code,
        device: device
      };
      this.dialogVisible = true;
    },

    confirmSliderValue() {
      const { device, fieldCode, value } = this.currentSlider;
      if (!device.data) {
        this.$set(device, 'data', {});
      }
      this.$set(device.data, fieldCode, value);
      this.dialogVisible = false;
    },

    getField(deviceId, fieldCode) {
      const device = this.deviceTemplates.find(d => d.id === deviceId);
      return device.fields.find(f => f.code === fieldCode);
    },

    getFieldMin(deviceId, fieldCode) {
      return this.fieldRanges[deviceId]?.[fieldCode]?.min || 0
    },

    getFieldMax(deviceId, fieldCode) {
      return this.fieldRanges[deviceId]?.[fieldCode]?.max || 100
    },

    getFieldStep(deviceId, fieldCode) {
      return this.fieldRanges[deviceId]?.[fieldCode]?.step || 1
    },

    generateRandomId(deviceType) {
      let prefix = '';

      console.log('deviceType', deviceType);
      
      // 根据设备类型设置前缀
      switch(deviceType) {
        case 'water-meter':
          prefix = 'WM_';
          break;
        case 'water-pipe':
          prefix = 'PP_';
          break;
        case 'water-pump':
          prefix = 'PM_';
          break;
        default:
          prefix = 'DEV_';
      }
      
      // 生成3位随机数字
      const randomNum = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
      return `${prefix}${randomNum}`;
    }
  }
}
</script>