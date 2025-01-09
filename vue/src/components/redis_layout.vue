<template>
  <div>
    <el-container>
      <!-- <el-header>Header</el-header> -->
      <!-- width的宽度跟collapse一样动态控制 -->
      <el-aside width="collapse">
        <!-- <h2>DBStack</h2> -->
        <el-menu
          :default-active="$route.path"
          router
          :collapse="isCollapse"
          class="el-menu-vertical"
          background-color="#393e42"
          text-color="#fff"
          active-text-color="rgb(64, 158, 255)"
        >
          <el-menu-item>
            <el-link type="primary" href="/home/mysql_instance" :underline="false"
              ><h2>DATAStack 控制台</h2></el-link
            >
          </el-menu-item>
          <!-- <el-menu-item>
            <span style="color: white">当前实例: {{ description }}</span></el-menu-item
          > -->

          <el-menu-item
            index="4"
            :route="{ path: '/home/redis/redis_detail', query: { ip: ip } }"
          >
            <i class="el-icon-s-grid"></i>
            <span slot="title">基本信息</span></el-menu-item
          >

          <el-menu-item
            index="4"
            :route="{ path: '/home/redis/redis_monitor', query: { ip: ip } }"
          >
            <i class="el-icon-s-platform"></i>
            <span slot="title">数据库监控</span></el-menu-item
          >
          <el-menu-item
            index="4"
            :route="{ path: '/home/redis/redis_adduser', query: { ip: ip } }"
          >
            <i class="el-icon-s-platform"></i>
            <span slot="title">用户管理</span></el-menu-item
          >
        </el-menu>
      </el-aside>
      <el-container>
        <!-- <el-aside width="100">Aside</el-aside> -->
        <el-header>
          <div :title="isCollapse ? '点击展开' : '点击收起'" class="box_bgd" @click="isC">
            <!-- 点击展开收起导航和切换对应图标 -->
            <i :class="!isCollapse ? 'el-icon-s-fold' : 'el-icon-s-unfold'"></i>
          </div>
        </el-header>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.el-header {
  background: #b3c0d1;
  color: #333;
  padding: 0 !important;
}

.el-aside {
  background: #393e42;
  color: #333;
  height: 100vh;
}
.el-menu {
  border-right-width: 0;
}
.el-main {
  color: #333;
}
.el-menu-vertical:not(.el-menu--collapse) {
  width: 240px;
}
.box_bgd {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.box_bgd i {
  font-size: 20px;
}
.box_bgd:hover {
  background: rgb(203, 215, 230);
}
</style>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
  data() {
    return {
      isCollapse: false, //默认为展开
      user: {
        name: "guofushan",
      },
      collapse: false,
      fullscreen: false,
      name: "linxin",
      message: 2,
      ip: this.$route.query.ip,
      description: this.$route.query.description,
    };
  },
  methods: {
    // 动态控制展开与收起和切换对应图标
    isC() {
      this.isCollapse = !this.isCollapse;
    },
  },
};
</script>
