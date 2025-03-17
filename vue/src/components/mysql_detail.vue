<template>
  <div class="flex flex-wrap gap-4">
    <el-card style="width: 100%">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
        </div>
      </template>
      <el-table
        :data="
          inventorys.filter(
            (data) => !search || data.ip.toLowerCase().includes(search.toLowerCase())
          )
        "
        border
        style="width: 100%"
        height="100"
      >
        <el-table-column label="名称" width="200" prop="description"> </el-table-column>
        <el-table-column label="数据库连接地址" width="260" prop="vip"> </el-table-column>
        <el-table-column label="端口" width="100" prop="port"> </el-table-column>
        <el-table-column label="MySQL部署IP" width="230" prop="ips"> </el-table-column>
        <el-table-column label="创建时间" prop="date_created"> </el-table-column>
      </el-table>
      <template #footer>Footer content</template>
    </el-card>

    <el-card style="width: 100%">
      <template #header>
        <div class="card-header">
          <span>运维管理</span>
        </div>
      </template>
      <el-table
        :data="
          orch.filter(
            (data) => !search || data.ip.toLowerCase().includes(search.toLowerCase())
          )
        "
        border
        style="width: 100%"
        height="100"
      >
        <el-table-column label="Orchestrator运维平台">
          <template #default="scope">
            <el-link
              target="_black"
              :underline="false"
              :href="scope.row.orch"
              prop="orch"
            >
              {{ scope.row.orch }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column label="Consul运维平台1">
          <template #default="scope">
            <el-link
              target="_black"
              :underline="false"
              :href="scope.row.consul1"
              prop="consul1"
            >
              {{ scope.row.consul1 }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column label="Consul运维平台2">
          <template #default="scope">
            <el-link
              target="_black"
              :underline="false"
              :href="scope.row.consul2"
              prop="consul2"
            >
              {{ scope.row.consul2 }}
            </el-link>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>Footer content</template>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      fullscreenLoading: false,
      search: "",
      inventorys: [],
      orch: [],
    };
  },
  created() {
    this.get_inventory();
  },
  methods: {
    get_inventory() {
      this.vip = this.$route.query.vip;

      this.$http
        .post("/api/mysql_detail/get_detail/", {
          vip: this.vip,
        })
        .then((res) => {
          if (res.data.status === true) {
            this.$message.success(res.data.msg);
            this.inventorys = res.data.data;
            this.orch = res.data.data1;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
