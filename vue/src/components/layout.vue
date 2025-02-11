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
            <i></i>
            <span slot="title"><h2>DATAStack</h2></span>
          </el-menu-item>

          <el-menu-item index="/home/mysql_instance">
            <i class="el-icon-menu"></i>
            <span slot="title">RDS MySQL</span>
          </el-menu-item>

          <el-menu-item index="/home/pg_instance">
            <i class="el-icon-menu"></i>
            <span slot="title">PostgreSQL</span>
          </el-menu-item>
          <el-menu-item index="/home/redis_instance">
            <i class="el-icon-menu"></i>
            <span slot="title">Redis</span>
          </el-menu-item>

          <el-submenu index="1">
            <template slot="title"
              ><i class="el-icon-s-tools"></i><span slot="title">运维中心</span></template
            >

            <el-menu-item-group>
              <el-menu-item index="/home/yunwei_center"
                ><i class="el-icon-share"></i>运维平台</el-menu-item
              >
            </el-menu-item-group>
            <el-menu-item-group>
              <el-menu-item index="/home/mysql_setmodify"
                ><i class="el-icon-setting"></i>设置</el-menu-item
              >
            </el-menu-item-group>
          </el-submenu>
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

<script>
export default {
  data() {
    return {
      isCollapse: false, //默认为展开
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
