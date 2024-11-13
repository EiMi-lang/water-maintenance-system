<template>
  <div class="fault-diagnosis">
    <!-- 搜索模块卡片 -->
    <div class="search-card">
      <div class="search-module">
        <div class="search-container">
          <el-select v-model="deviceType" placeholder="选择设备类型" style="width: 250px; margin-right: 20px;">
            <el-option label="水表设备" value="meter"></el-option>
            <el-option label="水泵设备" value="pump"></el-option>
            <el-option label="水管设备" value="pipe"></el-option>
          </el-select>
          <el-input v-model="deviceId" placeholder="输入设备ID或名称" style="width: 310px;">
            <el-button slot="append" @click="searchDevice">智能检修</el-button>
          </el-input>
        </div>
      </div>
    </div>

    <!-- 主体内容 -->
    <div class="main-content">
      <!-- 左侧内容 -->
      <div class="left-content">
        <!-- 设备分析 -->
        <div class="device-analysis">
          <h3>设备分析</h3>
          <div class="analysis-content">
            <div class="analysis-details">
              {{ device_analysis }}
            </div>
          </div>
        </div>

        <!-- 维护建议 -->
        <div class="maintenance-suggestions">
          <h3>预维护建议</h3>
          <div class="analysis-content">
            <div class="analysis-details">
              {{ this.device_maintain }}
            </div>
          </div>
        </div>
      </div>

      <!-- 文献参考区域 -->
      <div class="reference-section">
        <!-- 机器人LOGO -->
        <div class="robot-logo-container">
          <div class="robot-logo">
            <img src="@/assets/robot.gif" alt="AI机器人" class="robot-image" />
            <div class="glow-effect"></div>
            <div class="pulse-circle"></div>
          </div>
        </div>
        
        <!-- 文献参考 -->
        <div class="reference-docs">
          <h3>文献参考</h3>
          <div class="docs-content">
            <!-- 设备手册 -->
            <div class="doc-section">
              <h4>设备手册</h4>
              <ul>
                <li>
                  <i class="el-icon-document"></i>
                  <div class="doc-info">
                    <span class="doc-title">高压泵组操作手册 V2.1</span>
                    <span class="doc-meta">PDF | 8.5MB | 2024-01</span>
                  </div>
                  <el-button size="mini" type="primary" icon="el-icon-download">下载</el-button>
                </li>
                <li>
                  <i class="el-icon-document"></i>
                  <div class="doc-info">
                    <span class="doc-title">设备维护保养指南</span>
                    <span class="doc-meta">PDF | 5.2MB | 2024-02</span>
                  </div>
                  <el-button size="mini" type="primary" icon="el-icon-download">下载</el-button>
                </li>
              </ul>
            </div>

            <!-- 技术文档 -->
            <div class="doc-section">
              <h4>技术文档</h4>
              <ul>
                <li>
                  <i class="el-icon-notebook-2"></i>
                  <div class="doc-info">
                    <span class="doc-title">泵组性能参数说明书</span>
                    <span class="doc-meta">PDF | 3.1MB | 2024-01</span>
                  </div>
                  <el-button size="mini" type="primary" icon="el-icon-download">下载</el-button>
                </li>
                <li>
                  <i class="el-icon-notebook-2"></i>
                  <div class="doc-info">
                    <span class="doc-title">设备安装调试手册</span>
                    <span class="doc-meta">PDF | 4.7MB | 2024-02</span>
                  </div>
                  <el-button size="mini" type="primary" icon="el-icon-download">下载</el-button>
                </li>
              </ul>
            </div>

            <!-- 故障处理 -->
            <div class="doc-section">
              <h4>故障处理</h4>
              <ul>
                <li>
                  <i class="el-icon-warning-outline"></i>
                  <div class="doc-info">
                    <span class="doc-title">常见故障诊断手册</span>
                    <span class="doc-meta">PDF | 6.3MB | 2024-03</span>
                  </div>
                  <el-button size="mini" type="primary" icon="el-icon-download">下载</el-button>
                </li>
                <li>
                  <i class="el-icon-warning-outline"></i>
                  <div class="doc-info">
                    <span class="doc-title">紧急故障处理指南</span>
                    <span class="doc-meta">PDF | 2.8MB | 2024-03</span>
                  </div>
                  <el-button size="mini" type="primary" icon="el-icon-download">下载</el-button>
                </li>
              </ul>
            </div>

            <!-- 维护记录 -->
            <div class="doc-section">
              <h4>维护记录</h4>
              <ul>
                <li>
                  <i class="el-icon-time"></i>
                  <div class="doc-info">
                    <span class="doc-title">2024年Q1维护报告</span>
                    <span class="doc-meta">PDF | 1.5MB | 2024-03</span>
                  </div>
                  <el-button size="mini" type="primary" icon="el-icon-download">下载</el-button>
                </li>
                <li>
                  <i class="el-icon-time"></i>
                  <div class="doc-info">
                    <span class="doc-title">历史维护记录汇总</span>
                    <span class="doc-meta">Excel | 2.1MB | 2024-03</span>
                  </div>
                  <el-button size="mini" type="primary" icon="el-icon-download">下载</el-button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      device_analysis: '大模型分析中...',
      device_maintain: '大模型分析中...',
      device_desc: '',
      device_fault: '',
      searchQuery: '',
      deviceType: '',
      deviceId: '',
      documents: [
        { id: 1, title: '设备维护手册' },
        { id: 2, title: '故障处理指南' }
      ],
      maintenanceSuggestions: [
        { id: 1, content: '定期检查设备运行状态' },
        { id: 2, content: '更换老化部件' },
        // ... 其他建议
      ]
    }
  },

  created() {
    const { device_id, device_type,row } = this.$route.query
    this.deviceType = device_type
    this.deviceId = device_id

    if(this.deviceType == "meter"){
      this.device_desc = "这是一个水表设备，当前状态下的各个监控指标为:"
    } else if(this.deviceType == "pump"){
      this.device_desc = "这是一个水泵设备，当前状态下的各个监控指标为:"
    } else if(this.deviceType == "pipe"){
      this.device_desc = "这是一个水管设备，当前状态下的各个监控指标为:"
    }

    this.device_desc = this.device_desc.concat(JSON.stringify(row))
    this.loadDeviceAnalysis()
    this.loadMaintainAdvice()
  },
  methods: {
    async loadDeviceAnalysis() {
      const response = await axios.get(`http://localhost:8088/api/device/rag/${this.device_desc}`,
      {
        timeout: 30000,  // 增加超时时间到 30 秒
      }
      )
      if(response.data){
        this.device_analysis = response.data.answer
      }
      console.log("这是device_analysis",this.device_analysis)
    },
    async loadMaintainAdvice() {
      const response = await axios.get(`http://localhost:8088/api/device/maintain/${this.device_desc}`,
      {
        timeout: 30000,  // 增加超时时间到 30 秒
      })
      if(response.data){
        this.device_maintain = response.data.answer
      }
    },
    searchDevice() {
      console.log('搜索设备:', this.searchQuery);
    },
    downloadDoc(doc) {
      console.log('下载文档:', doc.title);
    }
  }
}
</script>

<style scoped>
.fault-diagnosis {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  padding: 20px;
  background: #fff;
  height: 100vh;
}

.search-card {
  background: #fff;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  height: 80px;
  display: flex;
  align-items: center;
}

.search-module {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-container {
  display: flex;
  align-items: center;
}

.main-content {
  display: grid;
  grid-template-columns: 2.2fr 0.8fr;
  gap: 20px;
  height: calc(100% - 80px);
}

.left-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  align-items: end;
}

.device-analysis, .maintenance-suggestions {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 40%;
}

.reference-docs {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: calc(100vh - 300px);
  overflow-y: auto;
  width: 90%;
  margin-left: auto;
}

h3 {
  margin-bottom: 10px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 5px;
}

a {
  color: #409EFF;
  cursor: pointer;
}

/* 确保没有其他样式干扰 */
.reference-section {
  position: relative;
  width: 100%;
  height: 100%;
}

.robot-logo-container {
  position: absolute;
  left: -1000px;  /* 调整位置，确保不会被裁剪 */
  top: 28%;
  transform: translateY(-50%);
  z-index: 1;
  width: 600px;  /* 明确设置容器宽度 */
  height: 600px; /* 明确设置��器高度 */
}

.robot-logo {
  position: relative;
  width: 100%;
  height: 100%;
}

/* 给图片添加特定的类名，提高优先级 */
.robot-image {
  width: 600px !important;  /* 使用!important确保优先级 */
  height: 600px !important;
  object-fit: contain;
  animation: float 3s ease-in-out infinite;
}

.glow-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 700px;
  height: 700px;
  background: radial-gradient(circle, rgba(45, 183, 245, 0.2) 0%, rgba(45, 183, 245, 0) 70%);
  border-radius: 50%;
  animation: glow 2s ease-in-out infinite;
}

.pulse-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 500px;
  height: 500px;
  border: 2px solid rgba(45, 183, 245, 0.3);
  border-radius: 50%;
  animation: pulse 2s ease-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes glow {
  0%, 100% { opacity: 0.5; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
}

@keyframes pulse {
  0% { transform: translate(-50%, -50%) scale(0.9); opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
}

.device-analysis {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 40%;
  overflow-y: auto;
}

.info-section {
  margin-bottom: 15px;
}

h4 {
  color: #409EFF;
  margin-bottom: 10px;
  font-size: 14px;
  border-left: 3px solid #409EFF;
  padding-left: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.info-item {
  display: flex;
  align-items: center;
}

.label {
  color: #666;
  margin-right: 8px;
  font-size: 13px;
  min-width: 70px;
}

.value {
  color: #333;
  font-size: 13px;
  font-weight: 500;
}

.status-normal {
  color: #67C23A;
}

.status-warning {
  color: #E6A23C;
}

.status-danger {
  color: #F56C6C;
}

.maintenance-suggestions {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 40%;
  overflow-y: auto;
}

.suggestions-content {
  height: calc(100% - 30px);
  overflow-y: auto;
}

.suggestion-section {
  margin-bottom: 15px;
}

h4 {
  color: #409EFF;
  margin-bottom: 10px;
  font-size: 14px;
  border-left: 3px solid #409EFF;
  padding-left: 10px;
}

h4.urgent {
  color: #F56C6C;
  border-left-color: #F56C6C;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  padding: 8px;
  border-radius: 4px;
  background: #fafafa;
  transition: all 0.3s;
}

li:hover {
  background: #f0f7ff;
}

li.urgent-item {
  background: #fff0f0;
  border-left: 3px solid #F56C6C;
}

li.urgent-item:hover {
  background: #fff6f6;
}

i {
  margin-right: 8px;
  font-size: 16px;
  color: #409EFF;
}

.urgent-item i {
  color: #F56C6C;
}

span {
  font-size: 13px;
  color: #606266;
  line-height: 1.4;
}

.urgent-item span {
  color: #F56C6C;
}

.doc-section {
  margin-bottom: 20px;
}

h4 {
  color: #409EFF;
  margin-bottom: 12px;
  font-size: 14px;
  border-left: 3px solid #409EFF;
  padding-left: 10px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  padding: 12px;
  border-radius: 4px;
  background: #f8f8f8;
  transition: all 0.3s;
}

li:hover {
  background: #f0f7ff;
}

i {
  font-size: 20px;
  color: #409EFF;
  margin-right: 12px;
}

.doc-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.doc-title {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
}

.doc-meta {
  font-size: 12px;
  color: #909399;
}

.el-button {
  padding: 7px 12px;
}

.el-button+.el-button {
  margin-left: 6px;
}

/* 添加到现有的 style 标签中 */

/* 通用卡片样式 */
.search-card,
.device-analysis,
.maintenance-suggestions,
.reference-docs {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 2px 12px 0 rgba(0, 0, 0, 0.05),
    0 0 10px rgba(64, 158, 255, 0.1);
}

/* 科技感边框效果 */
.search-card::before,
.device-analysis::before,
.maintenance-suggestions::before,
.reference-docs::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 2px solid transparent;
  border-radius: 8px;
  background: linear-gradient(45deg, 
    #409EFF, transparent 30%,
    transparent 70%, #409EFF 100%);
  -webkit-mask: 
    linear-gradient(#fff 0 0) content-box, 
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
  animation: borderAnimation 3s linear infinite;
}

/* 添加角落装饰 */
.search-card::after,
.device-analysis::after,
.maintenance-suggestions::after,
.reference-docs::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  border-top: 2px solid #409EFF;
  border-left: 2px solid #409EFF;
  top: 0;
  left: 0;
  animation: cornerPulse 2s infinite;
}

/* 右下角装饰 */
.search-card > div::after,
.device-analysis > div::after,
.maintenance-suggestions > div::after,
.reference-docs > div::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  border-bottom: 2px solid #409EFF;
  border-right: 2px solid #409EFF;
  bottom: 0;
  right: 0;
  animation: cornerPulse 2s infinite reverse;
}

/* 发光效果 */
.search-card,
.device-analysis,
.maintenance-suggestions,
.reference-docs {
  box-shadow: 0 0 10px rgba(64, 158, 255, 0.1);
  transition: box-shadow 0.3s ease;
}

.search-card:hover,
.device-analysis:hover,
.maintenance-suggestions:hover,
.reference-docs:hover {
  box-shadow: 
    0 4px 16px 0 rgba(0, 0, 0, 0.08),
    0 0 15px rgba(64, 158, 255, 0.2);
}

/* 边框动画 */
@keyframes borderAnimation {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 360% 50%;
  }
}

/* 角落脉冲动画 */
@keyframes cornerPulse {
  0% {
    opacity: 0.5;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
  100% {
    opacity: 0.5;
    transform: scale(1);
  }
}

/* 为标题添加渐变效果 */
h3, h4 {
  background: linear-gradient(45deg, #409EFF, #36cfc9);
  -webkit-background-clip: text;
  color: transparent;
  position: relative;
  display: inline-block;
}

/* 标题装饰线 */
h3::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #409EFF, transparent);
}

/* 确保内容不会被边框遮挡 */
.search-module,
.analysis-details,
.suggestions-content,
.docs-content {
  position: relative;
  z-index: 1;
}

/* 调整输入框和按钮样式 */
:deep(.el-input__inner) {
  height: 36px;
  line-height: 36px;
}

:deep(.el-input-group__append) {
  background-color: #409EFF;
  border-color: #409EFF;
  color: #fff;
  padding: 0 15px;
}

:deep(.el-input-group__append:hover) {
  background-color: #66b1ff;
  border-color: #66b1ff;
}

:deep(.el-select .el-input__inner) {
  border-radius: 4px;
}

.analysis-card {
  height: 45%;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin: 20px;
  transition: all 0.3s ease;
}

.analysis-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
}

.analysis-header {
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
  font-size: 16px;
  font-weight: bold;
  color: #409EFF;
  display: flex;
  align-items: center;
  gap: 8px;
}

.analysis-content {
  padding: 20px;
}

.analysis-details {
  line-height: 1.8;
  color: #606266;
  font-size: 14px;
  text-align: justify;
  white-space: pre-line;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  border-left: 4px solid #409EFF;
}

/* 添加响应式设计 */
@media screen and (max-width: 768px) {
  .analysis-card {
    margin: 10px;
  }
  
  .analysis-content {
    padding: 15px;
  }
  
  .analysis-details {
    font-size: 13px;
  }
}
</style>