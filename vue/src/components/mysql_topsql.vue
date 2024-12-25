<template>
  <el-row v-loading.fullscreen.lock="fullscreenLoading">
    <el-form
      label-position="left"
      label-width="100px"
      :model="ruleForm"
      :rules="rules"
      ref="ruleForm"
    >
    </el-form>
    <el-form label-position="left" label-width="100px">
      <el-form-item label="库名">
        <el-autocomplete
          clearable
          @focus="get_info"
          size="small"
          v-model="db_name"
          :debounce="0"
          :fetch-suggestions="schema_search"
          placeholder="dbname"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="时间范围">
        <el-date-picker
          size="small"
          type="datetime"
          placeholder="开始时间"
          v-model="start_time"
          value-format="yyyy-MM-dd HH:mm:ss"
          style="width: 25%"
        ></el-date-picker>
        -
        <el-date-picker
          size="small"
          type="datetime"
          placeholder="结束时间"
          v-model="stop_time"
          value-format="yyyy-MM-dd HH:mm:ss"
          style="width: 25%"
        ></el-date-picker>
        <el-button size="small" v-on:click="get_topsql()" round>查询</el-button>
      </el-form-item>
    </el-form>

    <el-table
      :data="detail_slow_logs.slice((currentPage - 1) * pagesize, currentPage * pagesize)"
      border
      style="width: 100%"
    >
      <el-table-column prop="hostip" label="IP" width="130"> </el-table-column>
      <el-table-column prop="schema_name" label="DB" width="100"> </el-table-column>
      <el-table-column
        prop="all_time"
        label="执行次数"
        width="100"
        sortable
      ></el-table-column>
      <el-table-column prop="min_time" label="开始时间" width="180"> </el-table-column>
      <el-table-column prop="max_time" label="结束时间" width="180"> </el-table-column>
      <el-table-column
        prop="digest_text"
        show-overflow-tooltip="true"
        label="SQL"
        sortable
      >
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="detail_slow_logs.length"
    >
    </el-pagination>
  </el-row>
</template>

<script>
import QS from "qs";
export default {
  // name: "binlog2sql",
  data() {
    return {
      timeout: null,
      currentPage: 1, //初始页
      pagesize: 10, // 每页的数据
      options: [],
      schema_lists: [],
      db_name: "",
      detail_slow_logs: [],
      fullscreenLoading: false,
      // only_schemas: "",
      start_time: "",
      stop_time: "",
      ruleForm: {
        host: "",
        start_file: "",
      },
      rules: {
        host: [{ required: true, message: "请输入主机地址", trigger: "blur" }],
      },
    };
  },
  methods: {
    handleSizeChange: function (size) {
      this.pagesize = size;
      console.log(this.pagesize); //每页下拉显示数据
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
      console.log(this.currentPage); //点击第几页
    },

    schema_search(queryString, cb) {
      var schema_lists = this.schema_lists;
      var results = queryString
        ? schema_lists.filter(this.createFilter(queryString))
        : schema_lists;
      cb(results);
    },

    createFilter(queryString) {
      return (list) => {
        return list.value.toLowerCase().indexOf(queryString.toLowerCase()) !== -1;
      };
    },
    // handleSelect(item) {
    //   console.log(item)
    // },
    // 页面输入主机地址，后端返回该主机的binlog文件和所有的数据库
    get_info() {
      this.vip = this.$route.query.vip;
      this.db_name = "";
      this.schema_lists = [];
      this.$http
        .post("/api/mysql_topsql/auto_complete/", {
          host: this.vip,
          // only_schemas: "",
        })
        .then((response) => {
          if (response.data.status === true) {
            for (let i of response.data.data.schemas) {
              this.schema_lists.push({ value: i });
            }
          } else {
            this.$message.error(response.data.msg);
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    get_topsql() {
      this.vip = this.$route.query.vip;
      // console.log(this.time);
      this.fullscreenLoading = true;
      this.$http
        .post("/api/mysql_topsql/get_top_sql/", {
          start_time: this.start_time,
          stop_time: this.stop_time,
          hostip: this.vip,
          db_name: this.db_name,
        })
        .then(
          function (res) {
            if (res.data.status === false) {
              this.$message.error(res.data.msg);
            } else {
              this.$message.success(res.data.msg);
              this.fullscreenLoading = false;
              this.detail_slow_logs = res.data.data;
            }
          }.bind(this)
        )
        .catch(function (error) {
          console.log(error);
        });
    },
  },
  // 钩子函数
  created() {
    // this.get_all_db_ips();
  },
};
</script>

<style>
.el-form-item {
  /* 设置控件之间的间距 */
  margin-top: -5px;
}
.el-autocomplete {
  width: 25%;
}
.el-select {
  width: 25%;
}
</style>
