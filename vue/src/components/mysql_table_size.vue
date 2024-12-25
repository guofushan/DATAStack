<template>
  <el-tabs type="border-card" v-model="activeName">
    <el-tab-pane label="Top 30" name="first">
      <hr />
      <el-table
        :data="
          schedulers.filter(
            (data) => !search || data.command.toLowerCase().includes(search.toLowerCase())
          )
        "
        :row-class-name="jobtableRowClassName"
        border
        height="700"
      >
        <el-table-column label="表名" width="300" prop="tablename"> </el-table-column>
        <el-table-column label="表大小(GB)" width="100" prop="tablesize" sortable>
        </el-table-column>
        <el-table-column label="VIP" width="150" prop="hostip"> </el-table-column>
        <el-table-column label="行数" width="150" prop="TABLE_ROWS" sortable>
        </el-table-column>
      </el-table>
    </el-tab-pane>

    <el-tab-pane label="实例表空间TOP" name="second">
      <el-row style="padding-bottom: 30px">
        <!-- <span class="demonstration">时间范围</span> -->
        <el-select v-model="ip" size="mini" filterable placeholder="请选择IP">
          <el-option
            v-for="item in options"
            :key="item.vip"
            :label="item.vip"
            :value="item.vip"
          ></el-option>
        </el-select>
        <el-button
          size="medium"
          type="primary"
          vicon="el-icon-search"
          @click="get_ins_detail()"
          round
          >查询</el-button
        >
      </el-row>
      <el-table
        :data="
          detail_table.filter(
            (data) => !search || data.command.toLowerCase().includes(search.toLowerCase())
          )
        "
        style="width: 100%"
        :row-class-name="jobtableRowClassName"
        border
        height="700"
      >
        <el-table-column label="表名" width="250" prop="tablename"> </el-table-column>
        <el-table-column label="表大小(GB)" width="100" prop="tablesize" sortable>
        </el-table-column>
        <el-table-column label="VIP" width="350" prop="hostip"> </el-table-column>
        <el-table-column label="行数" width="150" prop="TABLE_ROWS" sortable>
        </el-table-column>
      </el-table>
    </el-tab-pane>

    <el-tab-pane label="MySQL实例排行榜" name="third">
      <hr />
      <el-table
        :data="
          insinfo.filter(
            (data) => !search || data.command.toLowerCase().includes(search.toLowerCase())
          )
        "
        :row-class-name="jobtableRowClassName"
        border
        height="700"
      >
        <el-table-column label="VIP" width="250" prop="vip"> </el-table-column>
        <el-table-column label="实例大小(GB)" width="130" prop="ins_size" sortable>
        </el-table-column>
        <el-table-column label="集群信息" width="300" prop="ip"> </el-table-column>
      </el-table>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
export default {
  data() {
    return {
      activeName: "first",
      search: "",
      schedulers: [],
      schedulers_detail: [],
      options: [],
      ip: "",
      detail_table: [],
      insinfo: [],
    };
  },
  created() {
    // this.get_all_table();
    this.get_tableinfo();
    this.get_ips();
    this.get_insinfo();
  },
  methods: {
    get_tableinfo() {
      this.$http
        .post("/api/table_size/get_tableinfo/")
        .then((res) => {
          if (res.data.status === true) {
            console.log(res);
            this.$message.success(res.data.msg);
            this.schedulers = res.data.data;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    get_insinfo() {
      this.$http
        .post("/api/table_size/get_insinfo/")
        .then((res) => {
          if (res.data.status === true) {
            console.log(res);
            this.$message.success(res.data.msg);
            this.insinfo = res.data.data;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    get_ips() {
      this.$http
        .post("/api/table_size/get_ip/")
        .then((res) => {
          if (res.data.status === false) {
            this.$message.error(res.data.msg);
          } else {
            this.options = res.data.data;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    get_ins_detail() {
      this.fullscreenLoading = true;
      this.$http
        .post("/api/table_size/get_detail/", { db_ips: this.ip })
        .then((res) => {
          if (res.data.status === false) {
            this.$message.error(res.data.msg);
          } else {
            this.$message.success(res.data.msg);
            this.fullscreenLoading = false;
            this.detail_table = res.data.data;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
};
</script>
<style>
.el-table .warning-row {
  background: oldlace;
}
</style>
