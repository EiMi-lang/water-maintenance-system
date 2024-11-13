<template>
  <div class="device-details">
    <!-- 整合后的搜索和信息展示区域 -->
    <div class="search-container">
      <div class="search-box">
        <div class="search-header">
          <div class="header-title">
            <i class="el-icon-monitor pulse-icon"></i>
            <span>设备详情查询</span>
          </div>
        </div>
        
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="设备类型" class="search-item">
            <el-select 
              v-model="searchForm.deviceType" 
              placeholder="请选择设备类型"
              class="custom-select"
            >
              <el-option 
                v-for="item in deviceTypes" 
                :key="item.value" 
                :label="item.label" 
                :value="item.value"
              >
                <span class="device-type-option">
                  <i :class="item.icon"></i>
                  {{ item.label }}
                </span>
              </el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="设备ID" class="search-item">
            <el-input 
              v-model="searchForm.deviceId" 
              placeholder="请输入设备ID"
              class="custom-input"
            >
              <i slot="prefix" class="el-icon-cpu"></i>
            </el-input>
          </el-form-item>
          
          <el-button 
            type="primary" 
            @click="handleSearch"
            class="search-button"
            :loading="loading"
          >
            <i class="el-icon-search"></i>
            搜索
          </el-button>
          <el-button 
            @click="handleReset"
            class="reset-button"
          >
            <i class="el-icon-refresh"></i>
            重置
          </el-button>
        </el-form>
      </div>
    </div>

    <!-- 图表展示区域 -->
    <div class="charts-container">
      <!-- 流量趋势图 -->
      <el-card class="chart-card">
        <div class="chart-header">
          <h3>流量趋势</h3>
          <el-radio-group v-model="timeRange" size="small">
            <el-radio-button label="4h">4小时</el-radio-button>
            <el-radio-button label="8h">8小时</el-radio-button>
            <el-radio-button label="12h">12小时</el-radio-button>
          </el-radio-group>
        </div>
        <div ref="tempChart" class="chart"></div>
      </el-card>

      <!-- 综合时序数据图表 -->
      <el-card class="chart-card">
        <div class="chart-header">
          <h3>综合时序数据</h3>
          <el-radio-group v-model="timeRange" size="small">
            <el-radio-button label="4h">4小时</el-radio-button>
            <el-radio-button label="8h">8小时</el-radio-button>
            <el-radio-button label="12h">12小时</el-radio-button>
          </el-radio-group>
        </div>
        <div ref="combinedTimeSeriesChart" class="chart"></div>
      </el-card>

      <!-- 故障概率趋势柱状图 -->
      <el-card class="chart-card">
        <div class="chart-header">
          <h3>故障概率趋势</h3>
          <el-radio-group v-model="timeRange" size="small">
            <el-radio-button label="4h">4小时</el-radio-button>
            <el-radio-button label="8h">8小时</el-radio-button>
            <el-radio-button label="12h">12小时</el-radio-button>
          </el-radio-group>
        </div>
        <div ref="vibChart" class="chart"></div>
      </el-card>

      <!-- 故障分布饼图 -->
      <el-card class="chart-card">
        <h3>故障类型分布</h3>
        <div ref="faultPieChart" class="chart"></div>
      </el-card>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import axios from 'axios'

export default {
  name: 'DeviceDetails',
  data() {
    return {
      faultPieData: [],
      faultProbData: [],
      tempData: [],
      shakeData: [],
      humidityData: [],
      powerData: [],
      noiseData: [],
      signalData: [],
      voltageData: [],
      timeRangeData: [],
      pressureData: [],
      pipPressureData: [],
      deviceFluxLogs: [],
      deviceId: this.$route.params.deviceId,
      deviceData: this.$route.params.deviceData || {},
      timeRange: '4h',
      charts: {},
      searchForm: {
        deviceType: 'meter',
        deviceId: 'WM_001'
      },
      loading: false,
      deviceTypes: [
        {
          label: '水表设备',
          value: 'meter',
          icon: 'el-icon-odometer'
        },
        {
          label: '水泵设备',
          value: 'pump',
          icon: 'el-icon-help'
        },
        {
          label: '水管设备',
          value: 'pipe',
          icon: 'el-icon-connection'
        }
      ]
    }
  },
  mounted() {
    //this.initCharts()
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
    Object.values(this.charts).forEach(chart => chart.dispose())
  },
  created() {
    // 在组件创建时获取路由参数并设置表单值
    const { device_id, device_type } = this.$route.query
    if (device_id) {
      this.searchForm.deviceId = device_id
    }
    if (device_type) {
      this.searchForm.deviceType = device_type
    }
    
    // 获取设备详情数据
    this.loadFluxData()
    this.loadCombinedTimeSeriesData()
    this.loadFaultProbabilityData()
    this.loadFaultPieData()
  },
  methods: {
    initCharts() {
      this.initFlowTrendChart()
      this.initCombinedTimeSeriesChart()
      this.loadFaultProbabilityData()
      this.loadFaultPieData()
    },
    // 综合时序数据图表的初始化方法
    initCombinedTimeSeriesChart() {
      const chart = echarts.init(this.$refs.combinedTimeSeriesChart)
      this.charts.combinedTimeSeries = chart

      // 根据设备类型选择要展示的系列
      let series = []
      const deviceType = this.searchForm.deviceType

      if (deviceType === 'meter') {
        series = [
          {
            name: '压力',
            type: 'bar',
            stack: '总量',
            //smooth: true,
            //lineStyle: { width: 0 },
            //showSymbol: false,
            itemStyle: {
              borderRadius: [4, 4, 0, 0],
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgb(255, 191, 0)' },
                { offset: 1, color: 'rgb(224, 62, 76)' }
              ])
            },
            data: this.pressureData
          },
          {
            name: '信号强度',
            type: 'bar',
            stack: '总量',
            //smooth: true,
            //lineStyle: { width: 0 },
            //showSymbol: false,
            itemStyle: {
              borderRadius: [4, 4, 0, 0],
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgb(0, 221, 255)' },
                { offset: 1, color: 'rgb(77, 119, 255)' }
              ])
            },
            data: this.signalData
          },
          {
            name: '电压',
            type: 'bar',
            stack: '总量',
            //smooth: true,
            //lineStyle: { width: 0 },
            //showSymbol: false,
            itemStyle: {
              borderRadius: [4, 4, 0, 0],
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgb(55, 162, 255)' },
                { offset: 1, color: 'rgb(116, 21, 219)' }
              ])
            },
            data: this.voltageData
          }
        ]
      } else if (deviceType === 'pipe') {
        series = [
          {
            name: '压力',
            type: 'bar',
            stack: '总量',
            //smooth: true,
            //lineStyle: { width: 0 },
            //showSymbol: false,
            itemStyle: {
              borderRadius: [4, 4, 0, 0],
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgb(255, 191, 0)' },
                { offset: 1, color: 'rgb(224, 62, 76)' }
              ])
            },
            data: this.pipPressureData
          }
        ]
      } else if (deviceType === 'pump') {
        series = [
          {
            name: '温度',
            type: 'bar',
            stack: '总量',
            //smooth: true,
            //lineStyle: { width: 0 },
            //showSymbol: false,
            itemStyle: {
              borderRadius: [4, 4, 0, 0],
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgb(255, 191, 0)' },
                { offset: 1, color: 'rgb(224, 62, 76)' }
              ])
            },
            data: this.tempData
          },
          {
            name: '震动',
            type: 'bar',
            stack: '总量',
            //smooth: true,
            //lineStyle: { width: 0 },
            //showSymbol: false,
            itemStyle: {
              borderRadius: [4, 4, 0, 0],
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgb(255, 99, 132)' },
                { offset: 1, color: 'rgb(255, 159, 64)' }
              ])
            },
            data: this.shakeData
          },
          {
            name: '湿度',
            type: 'bar',
            stack: '总量',
            //smooth: true,
            //lineStyle: { width: 0 },
            //showSymbol: false,
            itemStyle: {
              borderRadius: [4, 4, 0, 0],
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgb(153, 102, 255)' },
                { offset: 1, color: 'rgb(201, 203, 207)' }
              ])
            },
            data: this.humidityData
          },
          {
            name: '功率',
            type: 'bar',
            stack: '总量',
            //smooth: true,
            //lineStyle: { width: 0 },
            //showSymbol: false,
            itemStyle: {
              borderRadius: [4, 4, 0, 0],
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgb(255, 206, 86)' },
                { offset: 1, color: 'rgb(255, 159, 64)' }
              ])
            },
            data: this.powerData
          },
          {
            name: '噪音',
            type: 'bar',
            stack: '总量',
            //smooth: true,
            //lineStyle: { width: 0 },
            //showSymbol: false,
            itemStyle: {
              borderRadius: [4, 4, 0, 0],
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgb(54, 162, 235)' },
                { offset: 1, color: 'rgb(75, 192, 192)' }
              ])
            },
            data: this.noiseData
          }
        ]
      }

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: series.map(s => s.name)
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: this.timeRangeData
        },
        yAxis: {
          type: 'value'
        },
        series: series,
        animationDuration: 1500,
        animationEasing: 'elasticOut'
      }

      chart.setOption(option)
    },
    // 初始化流量趋势
    initFlowTrendChart() {
      const chart = echarts.init(this.$refs.tempChart)
      this.charts.flow = chart

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'time',
          boundaryGap: false
        },
        yAxis: {
          type: 'value',
          name: '流量(m³/s)'
        },
        series: [{
          name: '流量',
          type: 'line',
          smooth: true,
          lineStyle: {
            width: 0
          },
          showSymbol: false,
          areaStyle: {
            opacity: 0.8,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgb(128, 255, 165)' },
              { offset: 1, color: 'rgb(1, 191, 236)' }
            ])
          },
          data: this.deviceFluxLogs
        }]
      }

      chart.setOption(option)
    },

    // 生成模拟时序数据
    generateTimeData() {
      const data = []
      let now = new Date()
      for (let i = 0; i < 24; i++) {
        data.push({
          value: [
            now.toLocaleString(),
            Math.round(Math.random() * 100)
          ]
        })
        now = new Date(+now + 3600 * 1000)
      }
      console.log("生成模拟时序数据",data)
      return data
    },


    // 加载流量数据
    async loadFluxData() {
      const response = await axios.get(`http://localhost:8088/api/device/${this.searchForm.deviceType}/${this.searchForm.deviceId}/flux`)
      if(response.data) {
        this.deviceFluxLogs = response.data.results
        this.initFlowTrendChart()
      }
    },

    // 加载综合时序数据
    async loadCombinedTimeSeriesData() {
      const response = await axios.get(`http://localhost:8088/api/device/${this.searchForm.deviceType}/${this.searchForm.deviceId}/details`)
      if(response.data) {
        if(this.searchForm.deviceType === 'meter') {
          this.pressureData = response.data.pressure
          this.signalData = response.data.signal
          this.voltageData = response.data.voltage
        } else if(this.searchForm.deviceType === 'pipe') {
          this.pipPressureData = response.data.pipe_pressure 
        } else if(this.searchForm.deviceType === 'pump') {
          this.tempData = response.data.temp
          this.shakeData = response.data.shake
          this.humidityData = response.data.humidity
          this.powerData = response.data.power
          this.noiseData = response.data.noise
        }

        this.timeRangeData = response.data.timestamp
        this.initCombinedTimeSeriesChart()
      }
    },

    //加载故障分布数据
    async loadFaultPieData() {
      const response = await axios.get(`http://localhost:8088/api/device/${this.searchForm.deviceType}/${this.searchForm.deviceId}/fault_pie`)
      if(response.data) {
        this.faultPieData = response.data.results
        this.initFaultPieChart()
      }
    },

    // 初始化故障分布折现图
    initFaultPieChart() {
      const chart = echarts.init(this.$refs.faultPieChart)
      this.charts.pie = chart
      
      const option = {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '故障类型',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '20',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: this.faultPieData
          }
        ]
      }
      
      chart.setOption(option)
    },
    // 处理窗口大小变化
    handleResize() {
      Object.values(this.charts).forEach(chart => chart.resize())
    },
    handleSearch() {
      this.loading = true;
      console.log('搜索条件：', this.searchForm);
      // 模拟搜索请求
      setTimeout(() => {
        this.loading = false;
        this.loadFluxData()
        this.loadCombinedTimeSeriesData()
        this.loadFaultProbabilityData()
        this.loadFaultPieData()
      }, 800);
    },
    handleReset() {
      this.searchForm.deviceType = 'meter';
      this.searchForm.deviceId = 'WM_001';
      this.loadFluxData()
      this.loadCombinedTimeSeriesData()
      this.loadFaultProbabilityData()
      this.loadFaultPieData()
    },
    
    async loadFaultProbabilityData() {
      const response = await axios.get(`http://localhost:8088/api/device/history/${this.searchForm.deviceType}/${this.searchForm.deviceId}/fault_prob`)
      if(response.data) {
        this.faultProbData = response.data.results
        console.log("故障概率数据",this.faultProbData)
        this.initFaultProbabilityLineChart()
      }
    },



    // 初始化故障概率趋势折线图
    initFaultProbabilityLineChart() {
      const chart = echarts.init(this.$refs.vibChart)
      this.charts.flow = chart

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          },
          formatter: function(params) {
            return `${params[0].name}<br/>${params[0].value[1]}`  // 修改tooltip显示格式
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'time',
          boundaryGap: false
        },
        yAxis: {
          type: 'value',
          name: '故障概率(%)'
        },
        series: [{
          name: '故障概率趋势',
          type: 'line',
          smooth: true,
          lineStyle: {
            width: 0
          },
          showSymbol: false,
          areaStyle: {
            opacity: 0.8,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgb(255, 191, 0)' },
              { offset: 1, color: 'rgb(224, 62, 76)' }
            ])
          },
          data: this.faultProbData.map(item => [
            item.name,  // 时间戳
            parseFloat(item.value[1].replace('%', ''))  // 去掉百分号并转为数字
          ])
          }]
        }

      chart.setOption(option)
    }
  },
  computed: {
    // 获取设备类型的显示文本
    getDeviceTypeLabel() {
      const deviceType = this.deviceTypes.find(
        type => type.value === this.searchForm.deviceType
      )
      return deviceType ? deviceType.label : '未知设备'
    },
    // 获取标签的类型
    getDeviceTagType() {
      const typeMap = {
        'waterMeter': 'success',
        'waterPump': 'warning',
        'waterPipe': 'info'
      }
      return typeMap[this.searchForm.deviceType] || 'info'
    }
  }
}
</script>

<style scoped>
.device-details {
  padding: 20px;
}

.detail-card {
  margin-bottom: 20px;
}

.device-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.device-title {
  font-size: 20px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 10px;
}

.device-info {
  margin-top: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.info-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.info-item .label {
  color: #666;
  margin-bottom: 5px;
}

.info-item .value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-card {
  position: relative;
  transition: all 0.3s ease;
}

.chart-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart {
  height: 350px;
}

h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

/* 响应式布局 */
@media screen and (max-width: 1200px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
}

@media screen and (max-width: 768px) {
  .device-info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
}

/* 新增搜索区域样式 */
.search-container {
  margin-bottom: 24px;
}

.search-box {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.search-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.search-header {
  margin-bottom: 20px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  color: #1a1a1a;
  font-weight: 600;
}

.pulse-icon {
  font-size: 24px;
  color: #409EFF;
  animation: pulse 2s infinite;
}

.search-form {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.search-item {
  margin-bottom: 0;
  margin-right: 16px;
}

.custom-select,
.custom-input {
  width: 220px;
}

:deep(.el-input__inner) {
  height: 40px;
  line-height: 40px;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s ease;
}

:deep(.el-input__inner:focus) {
  border-color: #409EFF;
  box-shadow: 0 0 8px rgba(64, 158, 255, 0.2);
}

.button-group {
  margin-left: auto;
  display: flex;
  gap: 12px;
}

.search-button,
.reset-button {
  height: 40px;
  padding: 0 24px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
}

.search-button {
  background: linear-gradient(135deg, #409EFF, #2e88ff);
  border: none;
}

.search-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.reset-button {
  border: 1px solid #dcdfe6;
}

.reset-button:hover {
  border-color: #409EFF;
  color: #409EFF;
}

.reset-button i {
  transition: transform 0.3s ease;
}

.reset-button:hover i {
  transform: rotate(180deg);
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 添加下拉选项的样式 */
.device-type-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.device-type-option i {
  font-size: 16px;
  color: #409EFF;
}

/* 添加新的样式 */
.info-card {
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.info-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #303133;
}

.info-content {
  display: flex;
  gap: 40px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-item .label {
  color: #909399;
  font-size: 14px;
}

.info-item .value {
  color: #303133;
  font-size: 14px;
  font-weight: 500;
}

.pulse-icon {
  color: #409EFF;
  font-size: 20px;
}

/* 为不同设备类型设置不同的标签类型 */
.success {
  background-color: #f0f9eb;
  border-color: #e1f3d8;
}

.warning {
  background-color: #fef3f2;
  border-color: #fde2e2;
}

.info {
  background-color: #f4f4f5;
  border-color: #e9e9eb;
}
</style>