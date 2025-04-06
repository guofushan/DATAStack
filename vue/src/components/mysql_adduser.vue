<template>
  <el-row v-loading.fullscreen.lock="fullscreenLoading">
    <el-form label-position="left" label-width="120px">
      <el-form-item label="创建用户">
        <div class="input-size">
          <el-input placeholder="用户名" style="width: 25%" v-model="user_name" clearable>
          </el-input>
          <el-input
            size="medium"
            style="width: 25%"
            placeholder="授权IP"
            v-model="db_ip"
            clearable
          >
          </el-input>
          <nav></nav>
          <el-input
            size="medium"
            style="width: 25%"
            placeholder="密码"
            v-model="user_passwd"
            clearable
          >
          </el-input>
          <el-select v-model="db_name" multiple placeholder="数据库">
            <el-option
              v-for="item in mysqldbname"
              :key="item.dbs"
              :label="item.dbs"
              :value="item.dbs"
            >
            </el-option>
          </el-select>
          <el-select v-model="role_name" filterable placeholder="角色">
            <el-option
              v-for="item_1 in options_1"
              :key="item_1.role"
              :label="item_1.role"
              :value="item_1.role"
            >
            </el-option>
          </el-select>
          <el-button
            size="medium"
            type="primary"
            icon="el-icon-search"
            @click="create_user()"
            round
            >创建用户</el-button
          >
        </div>
      </el-form-item>
    </el-form>

    <el-table
      :data="detail_slow_logs.slice((currentPage - 1) * pagesize, currentPage * pagesize)"
      border
      :span-method="objectSpanMethod"
      style="width: 100%"
      height="500"
    >
      <el-table-column prop="grantee" label="user" width="150"> </el-table-column>
      <el-table-column prop="table_schema" label="授权DB" width="150"> </el-table-column>
      <el-table-column prop="grante" width="160" label="权限"> </el-table-column>
      <el-table-column prop="passwd" label="密码" width="150"> </el-table-column>
      <el-table-column width="180">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.$index, scope.row)"
            >修改密码</el-button
          >
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="详情" :visible.sync="dialogFormVisible" width="30%" center>
      <el-form :model="dialogdata" label-position="left" label-width="80px">
        <el-form-item label="用户">
          <el-input
            v-model="dialogdata.grantee"
            autocomplete="off"
            :disabled="true"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="dialogdata.passwd" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="save_inventory">确 定</el-button>
        <el-button @click="dialogFormVisible = false">取 消</el-button>
      </div>
    </el-dialog>
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
  data() {
    return {
      dialogFormVisible: false,
      dialogdata: {
        grantee: "",
        passwd: "",
      },
      timeout: null,
      currentPage: 1, //初始页
      pagesize: 10, // 每页的数据
      // options: [],
      options_1: [],
      mysqloptions: [],
      detail_slow_logs: [],
      mysqldbname: [],
      fullscreenLoading: false,
      username: "",
      mysql_ip: "",
      users: "",
      role_name: "",
      table_schema: "",
      ip: "",
      passwd: "",
      schema_name: "",
      grante: "",
      user_name: "",
      db_ip: "",
      user_passwd: "",
      db_name: [],
      vip: "",
    };
  },
  created: function () {
    this.get_topsql();
    // this.get_alldbname();
    this.get_role_name();
    this.get_dbname();
  },
  computed: {
    tableDataColumn() {
      const obj = {};
      this.detail_slow_logs.forEach((v, i) => {
        const grantee = v.grantee;
        if (obj[grantee]) {
          obj[grantee].push(i);
        } else {
          obj[grantee] = [];
          obj[grantee].push(i);
        }
      });

      return obj;
    },
  },
  methods: {
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if (columnIndex === 0) {
        if (rowIndex > 0 && row.grantee === this.detail_slow_logs[rowIndex - 1].grantee) {
          return {
            rowspan: 0,
            colspan: 0,
          };
        } else {
          const grantee = row.grantee;
          const rows = this.tableDataColumn[grantee];
          const length = rows.length;
          return {
            rowspan: length,
            colspan: 1,
          };
        }
      }
    },

    handleSizeChange: function (size) {
      this.pagesize = size;
      console.log(this.pagesize); //每页下拉显示数据
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
      console.log(this.currentPage); //点击第几页
    },

    get_topsql() {
      console.log(this.time);
      this.vip = this.$route.query.vip;
      this.fullscreenLoading = true;
      this.$http
        .post("/api/mysql_adduser/get_privilege/", {
          vip: this.vip,
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

    get_dbname() {
      this.vip = this.$route.query.vip;
      this.$http
        .post("/api/mysql_adduser/get_dbname/", {
          vip: this.vip,
        })
        .then((res) => {
          if (res.data.status === false) {
            this.$message.error(res.data.msg);
          } else {
            this.mysqldbname = res.data.data;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    get_role_name() {
      this.$http
        .post("/api/mysql_adduser/get_role/")
        .then((res) => {
          if (res.data.status === false) {
            this.$message.error(res.data.msg);
          } else {
            this.options_1 = res.data.data;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    create_user() {
      this.vip = this.$route.query.vip;
      this.fullscreenLoading = true;
      this.$http
        .post("/api/mysql_adduser/create_user/", {
          user_name: this.user_name,
          db_ip: this.db_ip,
          user_passwd: this.user_passwd,
          db_name: this.db_name.join(","),
          role_name: this.role_name,
          vip: this.vip,
        })
        .then((res) => {
          if (res.data.status === false) {
            this.$message.error(res.data.msg);
          } else {
            this.$message.success(res.data.msg);
            this.fullscreenLoading = false;
            this.detail_slow_logs = res.data.data;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    handleEdit(index, row) {
      this.$confirm("此操作将修改所有此用户的密码, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        this.dialogdata = row;
        this.dialogFormVisible = true;
      });
    },
    save_inventory() {
      // this.vip = this.$route.query.vip;
      this.postdata = {
        grantee: this.dialogdata.grantee,
        passwd: this.dialogdata.passwd,
        vip: this.$route.query.vip,
      };
      this.$http
        .post("/api/mysql_adduser/save_inventory/", this.postdata)
        .then((res) => {
          if (res.data.status === true) {
            this.dialogFormVisible = false;
            console.log(res);
            this.$message.success(res.data.msg);
            this.detail_slow_logs = res.data.data;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    handleDelete(index, row) {
      this.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.postdata = {
            // grantee: this.dialogdata.grantee,
            grantee: row.grantee,
            vip: this.$route.query.vip,
          };
          this.$http
            .post("/api/mysql_adduser/delete_inventory/", this.postdata)
            .then((res) => {
              if (res.data.status === true) {
                console.log(res);
                this.$message.success(res.data.msg);
                this.detail_slow_logs = res.data.data;
              } else {
                this.$message.error(res.data.msg);
              }
            })
            .catch((err) => {
              console.log(err);
            });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
  },
};
</script>
