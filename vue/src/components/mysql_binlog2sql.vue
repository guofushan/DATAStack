<template>
  <el-row v-loading.fullscreen.lock="fullscreenLoading">
    <el-form
      label-position="left"
      label-width="100px"
      :model="ruleForm"
      :rules="rules"
      ref="ruleForm"
    >
      <el-form-item label="binlog文件" prop="start_file">
        <el-autocomplete
          clearable
          @focus="get_info"
          size="small"
          v-model="ruleForm.start_file"
          :debounce="0"
          :fetch-suggestions="binlog_search"
          placeholder="请输入文件名"
        ></el-autocomplete>
      </el-form-item>
    </el-form>
    <el-form label-position="left" label-width="100px">
      <el-form-item label="库名">
        <el-autocomplete
          clearable
          size="small"
          v-model="only_schemas"
          :debounce="0"
          :fetch-suggestions="schema_search"
          placeholder="请输入库名"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="表名">
        <el-autocomplete
          clearable
          @focus="get_info"
          size="small"
          v-model="only_tables"
          :debounce="0"
          :fetch-suggestions="table_search"
          placeholder="请输入表名"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="时间范围">
        <el-date-picker
          size="small"
          type="datetime"
          placeholder="开始时间"
          v-model="start_time"
          style="width: 25%"
        ></el-date-picker>
        -
        <el-date-picker
          size="small"
          type="datetime"
          placeholder="结束时间"
          v-model="stop_time"
          style="width: 25%"
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="反解析">
        <el-checkbox v-model="flashback"></el-checkbox>
      </el-form-item>
      <el-form-item label="解析类型">
        <el-checkbox-group v-model="sql_type">
          <el-checkbox label="insert"></el-checkbox>
          <el-checkbox label="delete"></el-checkbox>
          <el-checkbox label="update"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>
    </el-form>
    <el-form>
      <el-form-item>
        <el-button size="small" type="primary" @click="analyze_binlog('ruleForm')"
          >开始解析</el-button
        >
        <el-button
          type="text"
          @click="download"
          v-if="download_link"
          style="position: relative; left: 50px"
          >解析成功!点此下载文件</el-button
        >
      </el-form-item>
    </el-form>
  </el-row>
</template>

<script>
import axios from "axios";

import QS from "qs";
export default {
  name: "binlog2sql",
  data() {
    return {
      timeout: null,
      // options: [],
      binlog_lists: [],
      schema_lists: [],
      table_lists: [],
      fullscreenLoading: false,
      download_link: false,
      only_schemas: "",
      only_tables: "",
      start_time: "",
      stop_time: "",
      flashback: false,
      sql_type: [],
      ruleForm: {
        host: "",
        start_file: "",
      },
      rules: {
        host: [{ required: true, message: "请输入主机地址", trigger: "blur" }],
        start_file: [
          { required: true, message: "请输入binlog文件名", trigger: "change" },
        ],
      },
    };
  },
  methods: {
    analyze_binlog(formName) {
      this.vip = this.$route.query.vip;

      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.download_link = false;
          this.fullscreenLoading = true;
          this.$http
            .post("/api/mysql_binlog2sql/get_binlog_info/", {
              // host: this.ruleForm.host,
              host: this.vip,
              start_file: this.ruleForm.start_file,
              only_schemas: this.only_schemas,
              only_tables: this.only_tables,
              start_time: this.start_time,
              stop_time: this.stop_time,
              flashback: this.flashback,
              sql_type: JSON.stringify(this.sql_type),
            })
            .then((response) => {
              if (response.data.status === true) {
                console.log(response);
                this.$message.success(response.data.msg);
                this.download_link = true;
                this.fullscreenLoading = false;
              } else {
                this.$message.error(response.data.msg);
                this.fullscreenLoading = false;
              }
            })
            .catch(function (error) {
              console.log(error);
            });
        } else {
          return false;
        }
      });
    },

    binlog_search(queryString, cb) {
      var binlog_lists = this.binlog_lists;
      var results = queryString
        ? binlog_lists.filter(this.createFilter(queryString))
        : binlog_lists;
      cb(results);
    },
    schema_search(queryString, cb) {
      var schema_lists = this.schema_lists;
      var results = queryString
        ? schema_lists.filter(this.createFilter(queryString))
        : schema_lists;
      cb(results);
    },
    table_search(queryString, cb) {
      var table_lists = this.table_lists;
      var results = queryString
        ? table_lists.filter(this.createFilter(queryString))
        : table_lists;
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
      this.binlog_lists = [];
      this.schema_lists = [];
      this.table_lists = [];
      this.$http
        .post("/api/mysql_binlog2sql/auto_complete/", {
          host: this.vip,
          only_schemas: this.only_schemas,
        })
        .then((response) => {
          if (response.data.status === true) {
            for (let i of response.data.data.schemas) {
              this.schema_lists.push({ value: i });
            }
            for (let j of response.data.data.binlog) {
              this.binlog_lists.push({ value: j });
            }
            for (let k of response.data.data.tables) {
              this.table_lists.push({ value: k });
            }
          } else {
            this.$message.error(response.data.msg);
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    download() {
      this.$http
        .post("/api/mysql_binlog2sql/download/", {
          responseType: "blob",
        })
        .then((res) => {
          const blob = new Blob([res.data]);
          const fileName = "binlog.sql";
          const alink = document.createElement("a");
          alink.download = fileName;
          alink.style.display = "none";
          alink.href = URL.createObjectURL(blob); // 这里是将文件流转化为一个文件地址
          document.body.appendChild(alink);
          alink.click();
          URL.revokeObjectURL(alink.href); // 释放URL 对象
          document.body.removeChild(alink);
        });
    },
  },
  created() {},
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
