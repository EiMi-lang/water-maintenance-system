<template>
  <div class="sidebar-container">
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="logo" class="logo-img"/>
      <div class="system-title">
        <h2>水务预测性维护系统</h2>
        <div class="underline"></div>
      </div>
    </div>

    <el-menu
      background-color="#1e1e2d"
      text-color="#fff"
      active-text-color="#409EFF"
      :router="true"
      class="custom-menu"
    >
      <el-menu-item index="fault-warning" class="menu-item">
        <i class="el-icon-warning"></i>
        <span>故障预警</span>
        <div class="hover-effect"></div>
      </el-menu-item>
      
      <el-menu-item index="/diagnosis" class="menu-item">
        <i class="el-icon-help"></i>
        <span>智能检修</span>
        <div class="hover-effect"></div>
      </el-menu-item>
      
      <el-menu-item index="/device-details" class="menu-item">
        <i class="el-icon-document"></i>
        <span>设备详情</span>
        <div class="hover-effect"></div>
      </el-menu-item>
      
      <el-menu-item index="/simulation" class="menu-item">
        <i class="el-icon-data-analysis"></i>
        <span>仿真输入</span>
        <div class="hover-effect"></div>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'Sidebar'
}
</script>

<style scoped>
.sidebar-container {
  height: 100vh;
  background: linear-gradient(180deg, #1e1e2d 0%, #2d2d44 100%);
  box-shadow: 3px 0 10px rgba(0, 0, 0, 0.2);
  width: 250px;
  position: relative;
  overflow: hidden;
}

.logo-container {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-img {
  width: 60px;
  height: 60px;
  margin-bottom: 10px;
  animation: rotate 20s linear infinite;
}

.system-title {
  position: relative;
  padding-bottom: 10px;
}

.system-title h2 {
  color: #fff;
  font-size: 1.2rem;
  margin: 0;
  background: linear-gradient(45deg, #409EFF, #36D1DC);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.underline {
  width: 50px;
  height: 3px;
  background: linear-gradient(90deg, #409EFF, #36D1DC);
  margin: 10px auto;
  border-radius: 2px;
  animation: width-change 2s ease-in-out infinite;
}

.custom-menu {
  border: none;
  margin-top: 20px;
}

.menu-item {
  position: relative;
  margin: 8px 0;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.menu-item:hover {
  background: rgba(64, 158, 255, 0.1) !important;
  transform: translateX(5px);
}

.menu-item i {
  margin-right: 10px;
  font-size: 20px;
  transition: all 0.3s ease;
}

.menu-item:hover i {
  transform: scale(1.2);
  color: #409EFF;
}

.hover-effect {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #409EFF, #36D1DC);
  transition: width 0.3s ease;
}

.menu-item:hover .hover-effect {
  width: 100%;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes width-change {
  0%, 100% {
    width: 50px;
  }
  50% {
    width: 100px;
  }
}

/* 添加菜单激活状态的样式 */
.el-menu-item.is-active {
  background: rgba(64, 158, 255, 0.2) !important;
  position: relative;
}

.el-menu-item.is-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background: #409EFF;
  border-radius: 0 4px 4px 0;
}

/* 添加霓虹灯效果 */
.el-menu-item.is-active i {
  text-shadow: 0 0 10px #409EFF;
}
</style>
