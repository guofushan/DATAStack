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
        <el-table-column label="名称" width="150" prop="description" sortable>
        </el-table-column>
        <el-table-column label="运行状态" width="80" prop="status">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status == '运行中' ? 'success' : 'warning'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="已用内存及配额" width="150" prop="details">
        </el-table-column>
        <el-table-column label="IP地址" prop="ip" width="150"> </el-table-column>

        <el-table-column label="端口" width="70" prop="port"> </el-table-column>
        <el-table-column label="密码" width="100" prop="pwd"> </el-table-column>

        <el-table-column label="版本" width="100" prop="redis_type"> </el-table-column>

        <el-table-column label="创建时间" prop="date_created"> </el-table-column>
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
      this.ip = this.$route.query.ip;
      this.$http
        .post("/api/redis_detail/get_detail/", {
          ip: this.ip,
        })
        .then((res) => {
          if (res.data.status === true) {
            this.$message.success(res.data.msg);
            this.inventorys = res.data.data;
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
