<template>
  <div class="fault-warning-container">
    <!-- 监控卡片部分 -->
    <div class="monitor-cards">
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="monitor-card fault-card">
            <div class="card-content">
              <div class="icon-section">
                <div class="icon-wrapper">
                  <i class="el-icon-watch"></i>
                </div>
              </div>
              <div class="info-section">
                <div class="card-title">水表监控</div>
                <div class="data-row">
                  <div class="data-item">
                    <div class="value-container">
                      <span class="number">{{ meterTotal }}</span>
                      <span class="label">设备总数</span>
                    </div>
                  </div>
                  <div class="divider"></div>
                  <div class="data-item">
                    <div class="value-container warning">
                      <span class="number">{{ meterAbnormal }}</span>
                      <span class="label">异常数量</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="monitor-card warning-card">
            <div class="card-content">
              <div class="icon-section">
                <div class="icon-wrapper">
                  <i class="el-icon-help"></i>
                </div>
              </div>
              <div class="info-section">
                <div class="card-title">水泵监控</div>
                <div class="data-row">
                  <div class="data-item">
                    <div class="value-container">
                      <span class="number">{{ pumpTotal }}</span>
                      <span class="label">设备总数</span>
                    </div>
                  </div>
                  <div class="divider"></div>
                  <div class="data-item">
                    <div class="value-container warning">
                      <span class="number">{{ pumpAbnormal }}</span>
                      <span class="label">异常数量</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="monitor-card normal-card">
            <div class="card-content">
              <div class="icon-section">
                <div class="icon-wrapper">
                  <i class="el-icon-connection"></i>
                </div>
              </div>
              <div class="info-section">
                <div class="card-title">水管监控</div>
                <div class="data-row">
                  <div class="data-item">
                    <div class="value-container">
                      <span class="number">{{ pipeTotal }}</span>
                      <span class="label">设备总数</span>
                    </div>
                  </div>
                  <div class="divider"></div>
                  <div class="data-item">
                    <div class="value-container warning">
                      <span class="number">{{ pipeAbnormal }}</span>
                      <span class="label">异常数量</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 表格Tab区域 -->
    <div class="table-tabs-container">
      <div class="section-header">
        <h3>设备监控中心</h3>
        <div class="header-line"></div>
      </div>

      <el-card class="table-card">
        <el-tabs v-model="activeTab" type="border-card" class="custom-tabs">
          <!-- 水表监控 -->
          <el-tab-pane name="meter">
            <span slot="label">
              <i class="el-icon-watch"></i> 水表监控
            </span>
            <div class="table-header">
              <div class="table-title">水表监控数据</div>
              <div class="header-operations">
                <el-input
                  v-model="searchQuery"
                  placeholder="请输入设备ID"
                  prefix-icon="el-icon-search"
                  clearable
                  size="small"
                  style="width: 170px; margin-right: 15px;"
                  @input="handleSearch"
                >
                </el-input>
                <el-button 
                  type="primary" 
                  icon="el-icon-refresh" 
                  circle
                  @click="refreshTable('meter')"
                  class="refresh-btn"
                ></el-button>
              </div>
            </div>
            <div class="table-container">
              <el-table 
                :data="meterData" 
                border 
                style="width: 100%"
                header-cell-class-name="table-header-cell"
                :default-sort="{prop: 'timestamp', order: 'descending'}"
              >
                <el-table-column 
                  prop="device_id" 
                  label="设备ID" 
                  min-width="150"
                  align="center"
                />
                <el-table-column 
                  prop="flux" 
                  label="流量(m³/h)" 
                  min-width="120"
                  align="center"
                />
                <el-table-column 
                  prop="pressure" 
                  label="压力(MPa)" 
                  min-width="120"
                  align="center"
                />
                <el-table-column 
                  prop="signal" 
                  label="信号强度(dB)" 
                  min-width="120"
                  align="center"
                />
                <el-table-column 
                  prop="voltage" 
                  label="电压(V)" 
                  min-width="120"
                  align="center"
                />
                <el-table-column 
                  prop="timestamp" 
                  label="采集时间" 
                  min-width="120"
                  align="center"
                />
                <el-table-column 
                  prop="fault_probability" 
                  label="故障概率(%)" 
                  min-width="120"
                  align="center"
                >
                  <template slot-scope="scope">
                    <span :class="{ 'warning-text': scope.row.fault_probability > 50 }">
                      {{ scope.row.fault_probability }}
                    </span>
                  </template>
                </el-table-column>
                <el-table-column 
                  prop="fault_types" 
                  label="故障类型" 
                  min-width="120"
                  align="center"
                >
                  <template slot-scope="scope">
                    <el-tag type="danger">
                      {{ scope.row.fault_types }}
                    </el-tag>
                  </template>
                </el-table-column>
                
                <!-- 操作�� -->
                <el-table-column 
                  label="操作" 
                  min-width="220"
                  align="center"
                  fixed="right"
                >
                  <template slot-scope="scope">
                    <el-button
                      type="primary"
                      size="mini"
                      class="cyber-button diagnosis-btn"
                      @click="navigateToDiagnosis(scope.row)"
                    >
                      <span class="cyber-button__glitch"></span>
                      <i class="el-icon-warning-outline"></i>
                      智能检修
                    </el-button>
                    <el-button
                      type="info"
                      size="mini"
                      class="cyber-button details-btn"
                      @click="handleDetails(scope.row)"
                    >
                      <span class="cyber-button__glitch"></span>
                      <i class="el-icon-document"></i>
                      设备详情
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>

              <!-- 分页器 -->
              <div class="pagination-container">
                <el-pagination
                  @size-change="handleWaterMeterSizeChange"
                  @current-change="handleWaterMeterCurrentChange"
                  :current-page="waterMeterCurrentPage"
                  :page-sizes="[10, 20, 30]"
                  :page-size="waterMeterPageSize"
                  :total="waterMeterTotal"
                  layout="total, sizes, prev, pager, next"
                />
              </div>
            </div>
          </el-tab-pane>

          <!-- 水管监控 -->
          <el-tab-pane name="pipe">
            <span slot="label">
              <i class="el-icon-connection"></i> 水管监控
            </span>
            <div class="table-header">
              <div class="table-title">水管监控数据</div>
              <div class="header-operations">
                <el-input
                  v-model="searchQuery"
                  placeholder="请输入设备ID"
                  prefix-icon="el-icon-search"
                  clearable
                  size="small"
                  style="width: 170px; margin-right: 15px;"
                  @input="handleSearch"
                >
                </el-input>
                <el-button 
                  type="primary" 
                  icon="el-icon-refresh" 
                  circle
                  @click="refreshTable('pipe')"
                  class="refresh-btn"
                ></el-button>
              </div>
            </div>
            <el-table 
              :data="pipeData" 
              border 
              style="width: 100%"
              header-cell-class-name="table-header-cell"
              :default-sort="{prop: 'timestamp', order: 'descending'}"
            >
              <el-table-column 
                prop="device_id" 
                label="设备ID" 
                min-width="150"
                align="center"
              />
              <el-table-column 
                prop="pipe_stage" 
                label="管段" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                prop="pipe_age" 
                label="管龄(年)" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                prop="pipe_diameter" 
                label="管径(mm)" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                prop="pipe_length" 
                label="管长(m)" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                prop="pipe_pressure" 
                label="压力(MPa)" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                prop="flux" 
                label="流量(m³/h)" 
                min-width="140"
                align="center"
              />
              <el-table-column 
                prop="bury_depth" 
                label="埋深(m)" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                  prop="timestamp" 
                  label="采集时间" 
                  min-width="130"
                  align="center"
              />
              <el-table-column 
                prop="fault_probability" 
                label="故障概率(%)" 
                min-width="120"
                align="center"
              >
                <template slot-scope="scope">
                  <span :class="{ 'warning-text': scope.row.fault_probability > 50 }">
                    {{ scope.row.fault_probability }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column 
                prop="fault_types" 
                label="故障类型" 
                min-width="120"
                align="center"
              >
                <template slot-scope="scope">
                  <el-tag type="warning">
                    {{ scope.row.fault_types }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <!-- 操作列 -->
              <el-table-column 
                label="操作" 
                min-width="220"
                align="center"
                fixed="right"
              >
                <template slot-scope="scope">
                  <el-button
                    type="primary"
                    size="mini"
                    class="cyber-button diagnosis-btn"
                    @click="navigateToDiagnosis(scope.row)"
                  >
                    <span class="cyber-button__glitch"></span>
                    <i class="el-icon-warning-outline"></i>
                    智能检修
                  </el-button>
                  <el-button
                    type="info"
                    size="mini"
                    class="cyber-button details-btn"
                    @click="handleDetails(scope.row)"
                  >
                    <span class="cyber-button__glitch"></span>
                    <i class="el-icon-document"></i>
                    设备详情
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination-container">
              <el-pagination
                @size-change="handleWaterPipeSizeChange"
                @current-change="handleWaterPipeCurrentChange"
                :current-page="waterPipeCurrentPage"
                :page-sizes="[10, 20, 30]"
                :page-size="waterPipePageSize"
                :total="waterPipeTotal"
                layout="total, sizes, prev, pager, next"
              />
            </div>
          </el-tab-pane>

          <!-- 水泵监控 -->
          <el-tab-pane name="pump">
            <span slot="label">
              <i class="el-icon-help"></i> 水泵监控
            </span>
            <div class="table-header">
              <div class="table-title">水泵监控数据</div>
              <div class="header-operations">
                <el-input
                  v-model="searchQuery"
                  placeholder="请输入设备ID"
                  prefix-icon="el-icon-search"
                  clearable
                  size="small"
                  style="width: 170px; margin-right: 15px;"
                  @input="handleSearch"
                >
                </el-input>
                <el-button 
                  type="primary" 
                  icon="el-icon-refresh" 
                  circle
                  @click="refreshTable('pump')"
                  class="refresh-btn"
                ></el-button>
              </div>
            </div>
            <el-table 
              :data="pumpData" 
              border 
              style="width: 100%"
              header-cell-class-name="table-header-cell"
              :default-sort="{prop: 'timestamp', order: 'descending'}"
            >
              <el-table-column 
                prop="device_id" 
                label="设备ID" 
                min-width="150"
                align="center"
              />
              <el-table-column 
                prop="temp" 
                label="温度(℃)" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                prop="shake" 
                label="震动(mm/s)" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                prop="humidity" 
                label="湿度(%)" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                prop="flux" 
                label="流量(m³/h)" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                prop="power" 
                label="功率(kW)" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                prop="noise" 
                label="噪音(dB)" 
                min-width="120"
                align="center"
              />
              <el-table-column 
                  prop="timestamp" 
                  label="采集时间" 
                  min-width="120"
                  align="center"
              />
              <el-table-column 
                prop="fault_probability" 
                label="故障概率(%)" 
                min-width="120"
                align="center"
              >
                <template slot-scope="scope">
                  <span :class="{ 'warning-text': scope.row.fault_probability > 50 }">
                    {{ scope.row.fault_probability }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column 
                prop="faultType" 
                label="故障类型" 
                min-width="120"
                align="center"
              >
                <template slot-scope="scope">
                  <el-tag type="warning">
                    {{ scope.row.fault_types }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <!-- 操作列 -->
              <el-table-column 
                label="操作" 
                min-width="220"
                align="center"
                fixed="right"
              >
                <template slot-scope="scope">
                  <el-button
                    type="primary"
                    size="mini"
                    class="cyber-button diagnosis-btn"
                    @click="navigateToDiagnosis(scope.row)"
                  >
                    <span class="cyber-button__glitch"></span>
                    <i class="el-icon-warning-outline"></i>
                    智能检修
                  </el-button>
                  <el-button
                    type="info"
                    size="mini"
                    class="cyber-button details-btn"
                    @click="handleDetails(scope.row)"
                  >
                    <span class="cyber-button__glitch"></span>
                    <i class="el-icon-document"></i>
                    设备详情
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination-container">
              <el-pagination
                @size-change="handleWaterPumpSizeChange"
                @current-change="handleWaterPumpCurrentChange"
                :current-page="waterPumpCurrentPage"
                :page-sizes="[10, 20, 30]"
                :page-size="waterPumpPageSize"
                :total="waterPumpTotal"
                layout="total, sizes, prev, pager, next"
              />
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.fault-warning-container {
  padding: 20px;
  background: #f0f2f5;
}

/* 监控卡片样式 */
.monitor-cards {
  margin-bottom: 20px;
}

.monitor-card {
  padding: 20px;
  border-radius: 8px;
  height: 160px;
  color: #fff;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.card-content {
  display: flex;
  height: 100%;
  align-items: center;
  gap: 20px;
}

.icon-section {
  padding: 0;
  margin: 0;
  transform: translateX(60%);
}

.icon-wrapper {
  width: 108px;
  height: 108px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.icon-wrapper::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
  animation: ripple 2.5s infinite;
}

.icon-wrapper i {
  font-size: 54px;
  color: #fff;
}

.info-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}

.card-title {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

.data-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}

.data-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.label {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 8px;
}

.value {
  font-size: 32px;
  font-weight: bold;
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.value small {
  font-size: 14px;
  opacity: 0.9;
}

.warning-value {
  color: #ffd700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
  animation: pulse 2s infinite;
}

.divider {
  width: 2px;
  height: 45px;
  background: rgba(255, 255, 255, 0.2);
}

/* 保持原有的动画效果 */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@keyframes ripple {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}

/* 保持原有的卡片渐变和悬停效果 */
.fault-card {
  background: linear-gradient(45deg, #ff6b6b, #ff8787);
}

.warning-card {
  background: linear-gradient(45deg, #ffd43b, #ffa94d);
}

.normal-card {
  background: linear-gradient(45deg, #69db7c, #38d9a9);
}

.monitor-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
  transition: all 0.3s ease;
}

.monitor-card:hover::before {
  transform: translateX(100%);
}

.monitor-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

.monitor-card:hover .ring-progress {
  stroke-dashoffset: 0 !important;
  transition: all 1.5s ease;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.abnormal-value {
  animation: pulse 2s infinite;
}

/* 表格相关样式 */
.table-tabs-container {
  margin-top: 20px;
}

.section-header {
  margin-bottom: 20px;
}

.section-header h3 {
  font-size: 24px;
  color: #1e1e2d;
  margin: 0;
  padding-bottom: 10px;
  background: linear-gradient(45deg, #409EFF, #36D1DC);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header-line {
  width: 120px;
  height: 3px;
  background: linear-gradient(90deg, #409EFF, #36D1DC);
  border-radius: 2px;
  animation: width-pulse 2s ease-in-out infinite;
}

.table-card {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.custom-tabs {
  background: #fff;
}

:deep(.el-tabs__item) {
  height: 50px;
  line-height: 50px;
  font-size: 16px;
  transition: all 0.3s;
}

:deep(.el-tabs__item:hover) {
  color: #409EFF;
  transform: translateY(-2px);
}

:deep(.el-tabs__item.is-active) {
  color: #409EFF;
  font-weight: bold;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  margin-bottom: 15px;
}

.table-title {
  font-size: 18px;
  font-weight: bold;
  color: #1e1e2d;
}

.refresh-btn {
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  transform: rotate(180deg);
  background: linear-gradient(45deg, #409EFF, #36D1DC);
}

.custom-table {
  margin-top: 15px;
}

:deep(.el-table th) {
  background-color: #f5f7fa;
  color: #1e1e2d;
  font-weight: bold;
}

:deep(.el-table__row) {
  transition: all 0.3s;
}

:deep(.el-table__row:hover) {
  transform: translateY(-2px);
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

:deep(.warning-row) {
  background: rgba(245, 108, 108, 0.1);
}

:deep(.alert-row) {
  background: rgba(230, 162, 60, 0.1);
}

@keyframes width-pulse {
  0%, 100% {
    width: 120px;
  }
  50% {
    width: 180px;
  }
}

/* 新增样式 */
.main-value {
  margin-bottom: 10px;
}

.sub-value {
  font-size: 14px;
  opacity: 0.9;
}

.abnormal-label {
  font-size: 14px;
}

.abnormal-value {
  font-size: 18px;
  font-weight: bold;
  margin: 0 5px;
}

.card-footer {
  position: absolute;
  bottom: 20px;
  left: 20px;
  right: 20px;
}

:deep(.el-progress-bar__outer) {
  background-color: rgba(255, 255, 255, 0.2) !important;
}

:deep(.el-progress__text) {
  color: #fff !important;
}

/* 调整内容布局 */
.card-content {
  display: flex;
  height: 100%;
  align-items: center;
  gap: 15px;
}

.info-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  text-align: center;
}

/* 数据行样式 */
.data-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}

.data-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.divider {
  width: 2px;
  height: 45px;
  background: rgba(255, 255, 255, 0.2);
}

.label {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 5px;
}

.value {
  font-size: 24px;
  font-weight: bold;
}

.value small {
  font-size: 12px;
  margin-left: 2px;
  opacity: 0.8;
}

.warning-value {
  color: #ffd700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
  animation: pulse 2s infinite;
}

/* 故障率环形进度条样式 */
.rate-section {
  display: flex;
  justify-content: center;
  margin-top: 5px;
}

.rate-ring {
  position: relative;
  width: 80px;
  height: 80px;
}

.rate-ring svg {
  transform: rotate(-90deg);
  overflow: visible;
}

.ring-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.1);
  stroke-width: 8;
}

.ring-progress {
  fill: none;
  stroke: #fff;
  stroke-width: 8;
  stroke-linecap: round;
  stroke-dasharray: 283;
  transition: stroke-dashoffset 1s ease;
  filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
}

.rate-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  width: 100%;
}

.rate-value {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 2px;
}

.rate-label {
  font-size: 12px;
  opacity: 0.8;
}

/* 动画效果 */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.rate-ring::before {
  content: '';
  position: absolute;
  top: -5px;
  left: -5px;
  right: -5px;
  bottom: -5px;
  border-radius: 50%;
  background: radial-gradient(circle at center, rgba(255,255,255,0.2) 0%, transparent 70%);
  animation: glow 2s infinite;
}

@keyframes glow {
  0% { opacity: 0.5; }
  50% { opacity: 1; }
  100% { opacity: 0.5; }
}

/* 保持原有的卡片悬停效果 */
.monitor-card:hover .ring-progress {
  stroke: #fff;
  filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.8));
}

/* 调整内容布局 */
.data-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
}

.data-item {
  display: flex;
  align-items: center;
}

/* 新增数值容器样式 */
.value-container {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.number {
  font-size: 32px;
  font-weight: bold;
  line-height: 1;
}

.label {
  font-size: 16px;
  opacity: 0.9;
}

.unit {
  font-size: 14px;
  opacity: 0.8;
  margin-left: 2px;
}

/* 异   数量的特殊式 */
.warning .number {
  color: #ffd700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
  animation: pulse 2s infinite;
}

.divider {
  width: 2px;
  height: 45px;
  background: rgba(255, 255, 255, 0.2);
}

/* 添加表头样式 */
.table-header-cell {
  background-color: #f5f7fa !important;
  color: #606266 !important;
  font-weight: bold !important;
  text-align: center !important;
}

.warning-text {
  color: #E6A23C;
  font-weight: bold;
}

/* 自定义按钮基础样式 */
.custom-button {
  margin: 0 5px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  border: none;
}

/* 故障诊断按钮样式 */
.diagnosis-btn {
  background: linear-gradient(45deg, #4CAF50, #45a049);
  box-shadow: 0 2px 5px rgba(76, 175, 80, 0.3);
}

.diagnosis-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(76, 175, 80, 0.4);
  background: linear-gradient(45deg, #45a049, #4CAF50);
}

.diagnosis-btn:active {
  transform: translateY(0);
}

/* 钮点击波纹效果 */
.custom-button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(255, 255, 255, .5);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%);
  transform-origin: 50% 50%;
}

.custom-button:focus:not(:active)::after {
  animation: ripple 1s ease-out;
}

@keyframes ripple {
  0% {
    transform: scale(0, 0);
    opacity: 1;
  }
  20% {
    transform: scale(25, 25);
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: scale(40, 40);
  }
}

/* 按钮内图标样式 */
.custom-button i {
  margin-right: 5px;
  font-weight: bold;
}

/* 按钮文字发光效果 */
.custom-button:hover {
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

/* 赛博朋克风格按钮 */
.cyber-button {
  --primary-color: #2196F3;
  --secondary-color: #45a049;
  position: relative;
  background: linear-gradient(
    45deg,
    var(--primary-color),
    var(--secondary-color)
  );
  border: 2px solid var(--primary-color);
  border-radius: 4px;
  color: #fff;
  text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  overflow: hidden;
}

.cyber-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: 0.5s;
}

.cyber-button:hover::before {
  left: 100%;
}

.cyber-button__glitch {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--primary-color);
  filter: blur(10px);
  opacity: 0;
  transition: 0.3s;
  pointer-events: none;
}

.cyber-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(33, 150, 243, 0.4);
}

.cyber-button:hover .cyber-button__glitch {
  opacity: 0.3;
  animation: glitch 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) both infinite;
}

@keyframes glitch {
  0% {
    transform: translate(0);
  }
  20% {
    transform: translate(-3px, 3px);
  }
  40% {
    transform: translate(-3px, -3px);
  }
  60% {
    transform: translate(3px, 3px);
  }
  80% {
    transform: translate(3px, -3px);
  }
  100% {
    transform: translate(0);
  }
}

.diagnosis-btn {
  --primary-color: #4CAF50;
  --secondary-color: #45a049;
  margin-right: 10px;
}

.details-btn {
  --primary-color: #2196F3;
  --secondary-color: #1976D2;
}

.warning-text {
  color: #E6A23C;
  font-weight: bold;
}

/* 表头样式 */
.table-header-cell {
  background-color: #f5f7fa !important;
  color: #606266 !important;
  font-weight: bold !important;
  text-align: center !important;
}

.table-container {
  padding: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.header-operations {
  display: flex;
  align-items: center;
}

.el-input-group__prepend {
  background-color: #fff;
}

.el-select .el-input {
  width: 120px;
}

/* 搜索框和下拉框样式优化 */
.el-input {
  --primary-color: #409EFF;
  --hover-color: #66b1ff;
}

.el-input >>> .el-input__inner {
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.el-input >>> .el-input__inner:hover {
  border-color: var(--hover-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.el-input >>> .el-input__inner:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 8px rgba(64, 158, 255, 0.2);
}

/* 下拉框样式优化 */
.el-select >>> .el-input__inner {
  border-right: none;
  background: linear-gradient(to right, #f5f7fa, #ffffff);
}

.el-select >>> .el-input.is-focus .el-input__inner {
  border-color: var(--primary-color);
}

/* 下拉选项样式 */
.el-select-dropdown__item {
  padding: 8px 20px;
  transition: all 0.3s;
}

.el-select-dropdown__item.hover,
.el-select-dropdown__item:hover {
  background: linear-gradient(to right, rgba(64, 158, 255, 0.1), rgba(64, 158, 255, 0.05));
}

.el-select-dropdown__item.selected {
  background: linear-gradient(to right, rgba(64, 158, 255, 0.2), rgba(64, 158, 255, 0.1));
  color: var(--primary-color);
  font-weight: bold;
}

/* 搜索图标样式 */
.el-input >>> .el-input__prefix {
  left: 140px;
  transition: all 0.3s;
}

.el-input >>> .el-input__prefix i {
  font-size: 16px;
  color: #909399;
  transition: all 0.3s;
}

.el-input:hover >>> .el-input__prefix i {
  color: var(--primary-color);
}

/* 清除按钮样式 */
.el-input >>> .el-input__suffix {
  transition: all 0.3s;
}

.el-input >>> .el-input__suffix i {
  transition: all 0.3s;
}

.el-input >>> .el-input__suffix i:hover {
  color: var(--primary-color);
  transform: rotate(90deg);
}

/* 添加搜索框激活时的动画效果 */
.el-input.is-active >>> .el-input__inner,
.el-input >>> .el-input__inner:focus {
  animation: glow 1.5s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    box-shadow: 0 0 5px rgba(64, 158, 255, 0.1),
                0 0 10px rgba(64, 158, 255, 0.1),
                0 0 15px rgba(64, 158, 255, 0.1);
  }
  to {
    box-shadow: 0 0 10px rgba(64, 158, 255, 0.2),
                0 0 20px rgba(64, 158, 255, 0.2),
                0 0 30px rgba(64, 158, 255, 0.2);
  }
}

/* 下拉面式 */
.el-select-dropdown {
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.el-select-dropdown__list {
  padding: 6px 0;
}
</style>

<script>
import axios from 'axios'

export default {
  name: 'FaultWarning',
  data() {
    return {
      activeTab: 'meter',
      faultCount: 5,    // 示例数据
      warningCount: 8,  // 示例数据
      normalCount: 87,  // 示例数据
      meterData: [],
      pipeData: [],
      pumpData: [],
      currentTableData: [],
      currentPage: 1,
      pageSize: 10,
      totalItems: 0,
      meterTotal: 0,
      meterAbnormal: 0,
      pumpTotal: 0,
      pumpAbnormal: 0,
      pipeTotal: 0,
      pipeAbnormal: 0,
      pipeTableData: this.generatePipeMockData(),
      pumpTableData: this.generatePumpMockData(),
      tableData: this.generateMeterData(),
      faultTypeTagMap: {
        // 水表故障类型
        '正常': 'success',
        '信号弱': 'warning',
        '电压低': 'warning',
        '流量异常': 'danger',
        '压力异常': 'danger',
        // 水管故障类型
        '管道泄漏': 'danger',
        '管道堵塞': 'danger',
        // 水泵故障类型
        '温度过高': 'danger',
        '震动异常': 'warning',
        '功率异常': 'warning',
        '噪音超标': 'danger'
      },
      // 水表监控分页数据
      waterMeterCurrentPage: 1,
      waterMeterPageSize: 10,
      waterMeterTotal: 30,
      allMeterData: [],

      // 水管监控分页数据
      waterPipeCurrentPage: 1,
      waterPipePageSize: 10,
      waterPipeTotal: 30,
      allPipeData: [],

      // 水泵监控分页数据
      waterPumpCurrentPage: 1,
      waterPumpPageSize: 10,
      waterPumpTotal: 30,
      allPumpData: [],

      // 搜索关的数据
      searchQuery: '',
      searchField: '',
      // 水表监控搜索字段
      meterSearchFields: [
        { label: '设备ID', value: 'deviceId' },
        { label: '压力', value: 'pressure' },
        { label: '流量', value: 'flowRate' },
        { label: '故障类型', value: 'faultType' }
      ],
      // 水管监控搜索字段
      pipeSearchFields: [
        { label: '设备ID', value: 'deviceId' },
        { label: '管段', value: 'pipeLevel' },
        { label: '管径', value: 'pipeDiameter' },
        { label: '故障类型', value: 'faultType' }
      ],
      // 水泵监控搜索字段
      pumpSearchFields: [
        { label: '设备ID', value: 'deviceId' },
        { label: '温度', value: 'temperature' },
        { label: '振动', value: 'vibration' },
        { label: '故障类型', value: 'faultType' }
      ],
    }
  },
  computed: {
    // 根据当前激活的tab返回对应的搜索字段
    searchFields() {
      if (this.$route.path.includes('meter')) {
        return this.meterSearchFields;
      } else if (this.$route.path.includes('pipe')) {
        return this.pipeSearchFields;
      } else {
        return this.pumpSearchFields;
      }
    }
  },
  created() {
    //this.loadData();
    //this.loadPipeData();
    //this.loadPumpData(); 
    this.fetchFaultWarningData();
  },
  methods: {
    async fetchFaultWarningData() {
      const response = await axios.get('http://localhost:8088/api/predict/devices/faults');

      if(response.data) {
        this.allMeterData = response.data.meterData.predictions;

        // meter分页
        const meterStart = (this.waterMeterCurrentPage - 1) * this.waterMeterPageSize;
        const meterEnd = meterStart + this.waterMeterPageSize;
        this.meterData = this.allMeterData.slice(meterStart, meterEnd);
        this.meterTotal = response.data.meterData.summary.total_devices;
        this.meterAbnormal = response.data.meterData.summary.warning_devices;
        this.waterMeterTotal = response.data.meterData.summary.total_devices;
      
        // pipe分页
        this.allPipeData = response.data.pipeData.predictions;
        const pipeStart = (this.waterPipeCurrentPage - 1) * this.waterPipePageSize;
        const pipeEnd = pipeStart + this.waterPipePageSize;
        this.pipeData = this.allPipeData.slice(pipeStart, pipeEnd);
        this.pipeTotal = response.data.pipeData.summary.total_devices;
        this.pipeAbnormal = response.data.pipeData.summary.warning_devices;
        this.waterPipeTotal = response.data.pipeData.summary.total_devices;

        // pump分页
        this.allPumpData = response.data.pumpData.predictions;
        const pumpStart = (this.waterPumpCurrentPage - 1) * this.waterPumpPageSize;
        const pumpEnd = pumpStart + this.waterPumpPageSize;
        this.pumpData = this.allPumpData.slice(pumpStart, pumpEnd);
        this.pumpTotal = response.data.pumpData.summary.total_devices;
        this.pumpAbnormal = response.data.pumpData.summary.warning_devices;
        this.waterPumpTotal = response.data.pumpData.summary.total_devices;
      }
      
    },

    generateMockData(type) {
      const data = [];
      const status = ['正常', '警告', '故障'];
      const locations = ['A区', 'B区', 'C区', 'D区'];
      
      for (let i = 1; i <= 30; i++) {
        const randomStatus = status[Math.floor(Math.random() * status.length)];
        const randomLocation = locations[Math.floor(Math.random() * locations.length)];
        
        let baseData = {
          id: `${type}-${i.toString().padStart(3, '0')}`,
          location: randomLocation,
          status: randomStatus,
          updateTime: new Date(Date.now() - Math.random() * 86400000).toLocaleString(),
          alertLevel: randomStatus === '正常' ? '低' : randomStatus === '警告' ? '中' : '高'
        };

        switch(type) {
          case 'meter':
            data.push({
              ...baseData,
              flowRate: (Math.random() * 100).toFixed(2),
              pressure: (Math.random() * 10).toFixed(2),
              temperature: (Math.random() * 30 + 10).toFixed(1)
            });
            break;
          case 'pipe':
            data.push({
              ...baseData,
              leakageRisk: (Math.random() * 100).toFixed(1) + '%',
              pressure: (Math.random() * 10).toFixed(2),
              vibration: (Math.random() * 5).toFixed(2)
            });
            break;
          case 'pump':
            data.push({
              ...baseData,
              powerConsumption: (Math.random() * 1000).toFixed(0),
              efficiency: (Math.random() * 30 + 70).toFixed(1) + '%',
              vibration: (Math.random() * 5).toFixed(2)
            });
            break;
        }
      }
      return data;
    },
    
    initData() {
      this.meterData = this.generateMockData('meter')
      this.pipeData = this.generateMockData('pipe')
      this.pumpData = this.generateMockData('pump')
    },
    
    refreshTable(type) {
      const loadingInstance = this.$loading({
        target: '.custom-table',
        background: 'rgba(255, 255, 255, 0.7)'
      });
      
      setTimeout(() => {
        switch(type) {
          case 'meter':
            this.meterData = this.generateMockData('meter');
            break;
          case 'pipe':
            this.pipeData = this.generateMockData('pipe');
            break;
          case 'pump':
            this.pumpData = this.generateMockData('pump');
            break;
        }
        loadingInstance.close();
        this.$message.success('数据已更新');
      }, 1000);
    },
    
    getStatusType(status) {
      switch(status) {
        case '正常': return 'success';
        case '警告': return 'warning';
        case '故障': return 'danger';
        default: return 'info';
      }
    },
    
    getAlertType(level) {
      switch(level) {
        case '': return 'success';
        case '中': return 'warning';
        case '高': return 'danger';
        default: return 'info';
      }
    },
    
    tableRowClassName({row}) {
      if (row.status === '故障') {
        return 'warning-row';
      } else if (row.status === '警告') {
        return 'alert-row';
      }
      return '';
    },
    
    handleSizeChange(val) {
      this.pageSize = val;
      this.currentPage = 1;
      this.loadData();
    },
    
    handleCurrentChange(val) {
      this.currentPage = val;
      this.loadData();
    },
    handleDiagnosis(row) {

    },
    generatePipeMockData() {
      const data = [];
      for (let i = 1; i <= 30; i++) {
        data.push({
          deviceId: `PP2024${i.toString().padStart(3, '0')}`,
          section: `A-${Math.floor(i/2 + 1)}`,
          age: Math.floor(Math.random() * 15 + 5),
          diameter: Math.floor(Math.random() * 200 + 100),
          length: Math.floor(Math.random() * 200 + 100),
          pressure: (Math.random() * 0.5 + 0.3).toFixed(2),
          instantFlow: (Math.random() * 20 + 10).toFixed(1),
          depth: (Math.random() * 2 + 1.5).toFixed(1),
          faultProbability: (Math.random() * 100).toFixed(1),
          faultType: this.getRandomFaultType()
        });
      }
      return data;
    },
    getRandomFaultType() {
      const types = ['正常', '压力异常', '流量异常', '管道泄漏', '管道堵塞'];
      return Math.random() < 0.7 ? '正常' : types[Math.floor(Math.random() * 4) + 1];
    },
    getFaultTypeTag(type) {
      return this.faultTypeTagMap[type] || 'info';
    },
    generatePumpMockData() {
      const data = [];
      for (let i = 1; i <= 30; i++) {
        data.push({
          deviceId: `PM2024${i.toString().padStart(3, '0')}`,
          temperature: Math.floor(Math.random() * 20 + 40), // 40-60℃
          vibration: (Math.random() * 0.3 + 0.1).toFixed(2), // 0.1-0.4mm/s
          humidity: Math.floor(Math.random() * 20 + 60),
          flowRate: (Math.random() * 15 + 15).toFixed(1), // 15-30m³/h
          power: (Math.random() * 2 + 4.5).toFixed(1), // 4.5-6.5kW
          noise: Math.floor(Math.random() * 15 + 70), // 70-85dB
          faultProbability: (Math.random() * 100).toFixed(1),
          faultType: this.getRandomPumpFaultType()
        });
      }
      return data;
    },
    getRandomPumpFaultType() {
      const types = ['正常', '温度过高', '震动异常', '功率异常', '噪音超标'];
      return Math.random() < 0.7 ? '正常' : types[Math.floor(Math.random() * 4) + 1];
    },
    generateMeterData() {
      const allData = [];
      // 生成30条数据
      for (let i = 1; i <= 30; i++) {
        // 随机生成故障类型，70%概率正常
        const faultTypes = ['正常', '信号弱', '电压低', '流量异常', '压力异常'];
        const faultType = Math.random() < 0.7 ? '正常' : faultTypes[Math.floor(Math.random() * 4) + 1];
        
        // 根据故障类型生成对应的数据
        let data = {
          deviceId: `WM${i.toString().padStart(3, '0')}`,
          flowRate: 0,
          pressure: 0,
          signalStrength: 0,
          voltage: 0,
          faultProbability: 0,
          faultType: faultType
        };

        // 根据故障类型设置不同的参数范围
        switch(faultType) {
          case '正常':
            data.flowRate = (Math.random() * 5 + 2).toFixed(2);  // 2-7
            data.pressure = (Math.random() * 0.3 + 0.8).toFixed(2);  // 0.8-1.1
            data.signalStrength = Math.floor(Math.random() * 20 + 75);  // 75-95
            data.voltage = (Math.random() * 0.2 + 3.5).toFixed(2);  // 3.5-3.7
            data.faultProbability = (Math.random() * 20).toFixed(1);  // 0-20
            break;
          case '信号弱':
            data.flowRate = (Math.random() * 5 + 2).toFixed(2);
            data.pressure = (Math.random() * 0.3 + 0.8).toFixed(2);
            data.signalStrength = Math.floor(Math.random() * 15 + 45);  // 45-60
            data.voltage = (Math.random() * 0.2 + 3.5).toFixed(2);
            data.faultProbability = (Math.random() * 20 + 60).toFixed(1);  // 60-80
            break;
          case '电压低':
            data.flowRate = (Math.random() * 5 + 2).toFixed(2);
            data.pressure = (Math.random() * 0.3 + 0.8).toFixed(2);
            data.signalStrength = Math.floor(Math.random() * 20 + 75);
            data.voltage = (Math.random() * 0.3 + 2.8).toFixed(2);  // 2.8-3.1
            data.faultProbability = (Math.random() * 20 + 60).toFixed(1);
            break;
          case '流量异常':
            data.flowRate = (Math.random() * 10 + 15).toFixed(2);  // 15-25
            data.pressure = (Math.random() * 0.3 + 0.8).toFixed(2);
            data.signalStrength = Math.floor(Math.random() * 20 + 75);
            data.voltage = (Math.random() * 0.2 + 3.5).toFixed(2);
            data.faultProbability = (Math.random() * 20 + 70).toFixed(1);  // 70-90
            break;
          case '压力异常':
            data.flowRate = (Math.random() * 5 + 2).toFixed(2);
            data.pressure = (Math.random() * 0.5 + 1.5).toFixed(2);  // 1.5-2.0
            data.signalStrength = Math.floor(Math.random() * 20 + 75);
            data.voltage = (Math.random() * 0.2 + 3.5).toFixed(2);
            data.faultProbability = (Math.random() * 20 + 70).toFixed(1);
            break;
        }
        allData.push(data);
      }
      return allData;
    },
    loadData() {
      const allData = this.generateMeterData();
      const start = (this.waterMeterCurrentPage - 1) * this.waterMeterPageSize;
      const end = start + this.waterMeterPageSize;
      this.meterData = allData.slice(start, end);
    },
    // 水表监控分页方法
    handleWaterMeterSizeChange(val) {
      this.waterMeterPageSize = val;
      this.waterMeterCurrentPage = 1;
      this.fetchFaultWarningData();
    },
    handleWaterMeterCurrentChange(val) {
      this.waterMeterCurrentPage = val;
      this.fetchFaultWarningData();
    },
    // 水管监控分页方法
    handleWaterPipeSizeChange(val) {
      this.waterPipePageSize = val;
      this.waterPipeCurrentPage = 1;
      this.fetchFaultWarningData();
    },
    handleWaterPipeCurrentChange(val) {
      this.waterPipeCurrentPage = val;
      this.fetchFaultWarningData();
    },
    // 水泵监控分页方法
    handleWaterPumpSizeChange(val) {
      this.waterPumpPageSize = val;
      this.waterPumpCurrentPage = 1;
      this.fetchFaultWarningData();
    },
    handleWaterPumpCurrentChange(val) {
      this.waterPumpCurrentPage = val;
      this.fetchFaultWarningData();
    },
    // 水管监控数据加载方法
    loadPipeData() {
      if (this.allPipeData.length === 0) {
        this.allPipeData = this.generatePipeData();
      }
      const start = (this.waterPipeCurrentPage - 1) * this.waterPipePageSize;
      const end = start + this.waterPipePageSize;
      this.pipeData = this.allPipeData.slice(start, end);
    },

    // 水泵监控数据加载方法
    loadPumpData() {
      if (this.allPumpData.length === 0) {
        this.allPumpData = this.generatePumpData();
      }
      const start = (this.waterPumpCurrentPage - 1) * this.waterPumpPageSize;
      const end = start + this.waterPumpPageSize;
      this.pumpData = this.allPumpData.slice(start, end);
    },

    // 生成水管监控数据
    generatePipeData() {
      const allData = [];
      // 生成30条水管数据
      for (let i = 1; i <= 30; i++) {
        // 随机生成故障类型，70%概率正常
        const faultTypes = ['正常', '漏水', '堵塞', '破损'];
        const faultType = Math.random() < 0.7 ? '正常' : faultTypes[Math.floor(Math.random() * 3) + 1];
        
        // 根据故障类型生成对应的数据
        let data = {
          deviceId: `WP${i.toString().padStart(3, '0')}`,  // 设备ID
          pipeLevel: ['主管', '支管', '连接管'][Math.floor(Math.random() * 3)],  // 管段
          pipeAge: Math.floor(Math.random() * 15 + 1),  // 管龄(年)
          pipeDiameter: [200, 300, 400, 500][Math.floor(Math.random() * 4)],  // 管径(mm)
          pipeLength: Math.floor(Math.random() * 500 + 100),  // 管长(m)
          pressure: 0,  // 压力(MPa)
          instantFlow: 0,  // 瞬时流量(m³/h)
          buriedDepth: Math.floor(Math.random() * 2 + 1),  // 埋深(m)
          faultProbability: 0,  // 故障概率(%)
          faultType: faultType  // 故障类型
        };

        // 根据故障类型设置不同的参数范围
        switch(faultType) {
          case '正常':
            data.pressure = (Math.random() * 0.3 + 0.5).toFixed(2);  // 0.5-0.8MPa
            data.instantFlow = (Math.random() * 5 + 2).toFixed(2);  // 2-7m³/h
            data.faultProbability = (Math.random() * 20).toFixed(1);  // 0-20%
            break;
          case '漏水':
            data.pressure = (Math.random() * 0.2 + 0.2).toFixed(2);  // 0.2-0.4MPa
            data.instantFlow = (Math.random() * 3 + 1).toFixed(2);  // 1-4m³/h
            data.faultProbability = (Math.random() * 20 + 60).toFixed(1);  // 60-80%
            break;
          case '堵塞':
            data.pressure = (Math.random() * 0.3 + 0.7).toFixed(2);  // 0.7-1.0MPa
            data.instantFlow = (Math.random() * 2 + 0.5).toFixed(2);  // 0.5-2.5m³/h
            data.faultProbability = (Math.random() * 20 + 70).toFixed(1);  // 70-90%
            break;
          case '破损':
            data.pressure = (Math.random() * 0.2 + 0.2).toFixed(2);  // 0.2-0.4MPa
            data.instantFlow = (Math.random() * 2 + 0.5).toFixed(2);  // 0.5-2.5m³/h
            data.faultProbability = (Math.random() * 20 + 70).toFixed(1);  // 70-90%
            break;
        }
        allData.push(data);
      }
      return allData;
    },
    // 生成水泵监控数据
    generatePumpData() {
      const allData = [];
      // 生成30条水泵数据
      for (let i = 1; i <= 30; i++) {
        // 随生成故障类，70%概率正常
        const faultTypes = ['正常', '振动异常', '温度过高', '噪音异常'];
        const faultType = Math.random() < 0.7 ? '正常' : faultTypes[Math.floor(Math.random() * 3) + 1];
        
        // 根据故障类型生成对应的数据
        let data = {
          deviceId: `PS${i.toString().padStart(3, '0')}`,  // 设备ID
          temperature: 0,  // 温度(℃)
          vibration: 0,  // 振动(mm/s)
          humidity: 0,  // 湿度(%)
          flowRate: 0,  // 流量(m³/h)
          power: 0,  // 功率(kW)
          noise: 0,  // 噪音(dB)
          faultProbability: 0,  // 故障概率(%)
          faultType: faultType  // 故障类型
        };

        // 根据故障类型设置不同的参数范围
        switch(faultType) {
          case '正常':
            data.temperature = Math.floor(Math.random() * 20 + 40);  // 40-60℃
            data.vibration = (Math.random() * 1 + 1).toFixed(2);  // 1-2mm/s
            data.humidity = Math.floor(Math.random() * 20 + 40);  // 40-60%
            data.flowRate = (Math.random() * 20 + 40).toFixed(1);  // 40-60m³/h
            data.power = (Math.random() * 5 + 15).toFixed(1);  // 15-20kW
            data.noise = Math.floor(Math.random() * 10 + 65);  // 65-75dB
            data.faultProbability = (Math.random() * 20).toFixed(1);  // 0-20%
            break;
          case '振动异常':
            data.temperature = Math.floor(Math.random() * 25 + 45);  // 45-70℃
            data.vibration = (Math.random() * 3 + 3).toFixed(2);  // 3-6mm/s
            data.humidity = Math.floor(Math.random() * 20 + 40);  // 40-60%
            data.flowRate = (Math.random() * 15 + 35).toFixed(1);  // 35-50m³/h
            data.power = (Math.random() * 6 + 17).toFixed(1);  // 17-23kW
            data.noise = Math.floor(Math.random() * 15 + 75);  // 75-90dB
            data.faultProbability = (Math.random() * 20 + 60).toFixed(1);  // 60-80%
            break;
          case '温度过高':
            data.temperature = Math.floor(Math.random() * 30 + 70);  // 70-100℃
            data.vibration = (Math.random() * 2 + 1.5).toFixed(2);  // 1.5-3.5mm/s
            data.humidity = Math.floor(Math.random() * 15 + 35);  // 35-50%
            data.flowRate = (Math.random() * 15 + 35).toFixed(1);  // 35-50m³/h
            data.power = (Math.random() * 7 + 18).toFixed(1);  // 18-25kW
            data.noise = Math.floor(Math.random() * 12 + 70);  // 70-82dB
            data.faultProbability = (Math.random() * 20 + 65).toFixed(1);  // 65-85%
            break;
          case '噪音异常':
            data.temperature = Math.floor(Math.random() * 25 + 45);  // 45-70℃
            data.vibration = (Math.random() * 2.5 + 2).toFixed(2);  // 2-4.5mm/s
            data.humidity = Math.floor(Math.random() * 20 + 40);  // 40-60%
            data.flowRate = (Math.random() * 20 + 35).toFixed(1);  // 35-55m³/h
            data.power = (Math.random() * 6 + 16).toFixed(1);  // 16-22kW
            data.noise = Math.floor(Math.random() * 20 + 85);  // 85-105dB
            data.faultProbability = (Math.random() * 20 + 70).toFixed(1);  // 70-90%
            break;
        }
        allData.push(data);
      }
      return allData;
    },
    // 搜索处理方法
    handleSearch() {
      if (!this.searchQuery) {
        // 搜索框为空时，恢复原始数据
        this.loadMeterData();
        this.loadPipeData();
        this.loadPumpData();
        return;
      }

      // 根据当前激活的tab执行对应的搜索
      if (this.$route.path.includes('meter')) {
        this.searchMeterData();
      } else if (this.$route.path.includes('pipe')) {
        this.searchPipeData();
      } else {
        this.searchPumpData();
      }
    },

    // 水表数据搜索
    searchMeterData() {
      const filteredData = this.allMeterData.filter(item => {
        const value = item[this.searchField];
        return value.toString().toLowerCase().includes(this.searchQuery.toLowerCase());
      });
      this.meterData = filteredData;
    },

    // 水管数据搜索
    searchPipeData() {
      const filteredData = this.allPipeData.filter(item => {
        const value = item[this.searchField];
        return value.toString().toLowerCase().includes(this.searchQuery.toLowerCase());
      });
      this.pipeData = filteredData;
    },

    // 水泵数据搜索
    searchPumpData() {
      const filteredData = this.allPumpData.filter(item => {
        const value = item[this.searchField];
        return value.toString().toLowerCase().includes(this.searchQuery.toLowerCase());
      });
      this.pumpData = filteredData;
    },
    handleDetails(row) {
      // 根据设备类型判断并设置对应的 deviceType
      let deviceType = 'meter' // 默认为水表设备
      
      // 根据设备编号或其他标识判断设备类型
      if (row.device_id.startsWith('WM')) {
        deviceType = 'meter' // 水表设备
      } else if (row.device_id.startsWith('PM')) {
        deviceType = 'pump' // 水泵设备
      } else if (row.device_id.startsWith('PP')) {
        deviceType = 'pipe' // 水管设备
      }
      
      // 跳转到设备详情页面
      this.$router.push({
        path: '/device-details',
        query: {
          device_id: row.device_id,
          device_type: deviceType
        }
      })
    },
    navigateToDiagnosis(row) {
      // 根据设备类型判断并设置对应的 deviceType
      let deviceType = 'meter' // 默认为水表设备
      
      // 根据设备编号或其他标识判断设备类型
      if (row.device_id.startsWith('WM')) {
        deviceType = 'meter' // 水表设备
      } else if (row.device_id.startsWith('PM')) {
        deviceType = 'pump' // 水泵设备
      } else if (row.device_id.startsWith('PP')) {
        deviceType = 'pipe' // 水管设备
      }

      // 跳转到智能检修页面
      this.$router.push({
        path: '/diagnosis',
        query: {
          device_id: row.device_id,
          device_type: deviceType,
          row: row
        }
      })
    }
  }
}
</script> 