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
            placeholder="密码"
            v-model="user_passwd"
            clearable
          >
          </el-input>
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
      <el-table-column prop="user_name" label="用户" width="150"> </el-table-column>
      <el-table-column prop="passwd" label="密码" width="150"> </el-table-column>
      <el-table-column prop="role" width="160" label="权限"> </el-table-column>
      <el-table-column prop="create_date" label="创建时间" width="250"> </el-table-column>
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
            v-model="dialogdata.user_name"
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
        user_name: "",
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
    this.get_role_name();
    this.get_topsql();
  },

  methods: {
    get_role_name() {
      this.$http
        .post("/api/redis_adduser/get_role/")
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
      this.ip = this.$route.query.ip;
      this.fullscreenLoading = true;
      this.$http
        .post("/api/redis_adduser/create_user/", {
          user_name: this.user_name,
          user_passwd: this.user_passwd,
          role_name: this.role_name,
          ip: this.ip,
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

    get_topsql() {
      console.log(this.time);
      this.ip = this.$route.query.ip;
      this.fullscreenLoading = true;
      this.$http
        .post("/api/redis_adduser/get_privilege/", {
          ip: this.ip,
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

    handleEdit(index, row) {
      this.$confirm("此操作将修改此用户的密码, 是否继续?", "提示", {
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
        user_name: this.dialogdata.user_name,
        passwd: this.dialogdata.passwd,
        ip: this.$route.query.ip,
      };
      this.$http
        .post("/api/redis_adduser/save_inventory/", this.postdata)
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
            user_name: row.user_name,
            ip: this.$route.query.ip,
          };
          this.$http
            .post("/api/redis_adduser/delete_inventory/", this.postdata)
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
