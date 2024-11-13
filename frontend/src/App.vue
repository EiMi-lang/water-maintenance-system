<template>
  <el-container class="app-wrapper">
    <el-aside width="260px">
      <sidebar></sidebar>
    </el-aside>
    <el-container>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue'

export default {
  name: 'App',
  components: {
    Sidebar
  }
}
</script>

<style>
.app-wrapper {
  height: 100vh;
}

.el-aside {
  background-color: #1e1e2d;
}

.el-main {
  background-color: #f5f7f9;
  padding: 20px;
}
</style>