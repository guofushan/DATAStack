<template>
  <div>
    <hr />
    <el-table
      :data="
        inventorys.filter(
          (data) => !search || data.ip.toLowerCase().includes(search.toLowerCase())
        )
      "
      border
      style="width: 100%"
      height="800"
    >
      <el-table-column width="260" type="index">
        <template slot="header">
          <el-dropdown>
            <el-button type="primary">
              创建实例<i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown"
              ><el-row
                ><el-button
                  type="warning"
                  icon="el-icon-plus"
                  size="small"
                  :style="{ float: 'left' }"
                  @click="
                    dialogFormVisible = true;
                    dialogdata = {
                      ip: '',
                      description: '',
                      port: '',
                      pwd: '',
                      buffer_pool_size: '',
                    };
                  "
                  >单实例</el-button
                ></el-row
              >
            </el-dropdown-menu>
          </el-dropdown>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" icon="el-icon-edit" @click="linkUpdate(scope.row)"
            >详情</el-button
          >
          <el-button size="mini" @click="handleEdit(scope.$index, scope.row)"
            >编辑</el-button
          >
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
            >删除实例</el-button
          >
        </template>
      </el-table-column>
      <el-table-column label="序列" width="60" type="index"> </el-table-column>
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
      <el-table-column label="IP地址" prop="ip" width="120"> </el-table-column>

      <el-table-column label="端口" width="70" prop="port"> </el-table-column>
      <el-table-column label="版本" width="100" prop="redis_type"> </el-table-column>

      <el-table-column label="创建时间" prop="date_created"> </el-table-column>
    </el-table>
    <el-dialog title="单实例" :visible.sync="dialogFormVisible" width="30%" center>
      <el-form :model="dialogdata" label-position="left" label-width="80px">
        <el-form-item label="IP地址">
          <el-input
            v-model="dialogdata.ip"
            autocomplete="off"
            placeholder="Redis IP"
          ></el-input>
        </el-form-item>
        <el-form-item label="PORT">
          <el-input
            v-model="dialogdata.port"
            autocomplete="off"
            placeholder="redis端口"
          ></el-input>
        </el-form-item>
        <el-form-item label="内存(GB)">
          <el-input
            v-model="dialogdata.buffer_pool_size"
            autocomplete="off"
            placeholder="redis maxmemory(填写数字即可)"
          ></el-input>
        </el-form-item>
        <el-form-item label="Redis密码">
          <el-input
            v-model="dialogdata.pwd"
            autocomplete="off"
            placeholder="密码"
          ></el-input>
        </el-form-item>
        <el-form-item label="实例名称">
          <el-input
            v-model="dialogdata.description"
            autocomplete="off"
            placeholder="描述业务、用途"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button
          type="primary"
          @click="save_inventory"
          v-loading.fullscreen.lock="fullscreenLoading"
          >确 定</el-button
        >
        <el-button @click="dialogFormVisible = false">取 消</el-button>
      </div>
    </el-dialog>

    <el-dialog title="单实例" :visible.sync="dialogFormVisible_modify" width="30%" center>
      <el-form :model="dialogdata_modify" label-position="left" label-width="80px">
        <el-form-item label="RDS备注">
          <el-input
            v-model="dialogdata_modify.description"
            autocomplete="off"
            placeholder="描述业务、用途"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button
          type="primary"
          @click="modify_rds"
          v-loading.fullscreen.lock="fullscreenLoading"
          >确 定</el-button
        >
        <el-button @click="dialogFormVisible_modify = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      fullscreenLoading: false,
      dialogFormVisible: false,
      dialogFormVisible_modify: false,
      dialogdata: {
        ip: "",
        description: "",
        port: "",
        pwd: "",
        buffer_pool_size: "",
      },
      dialogdata_modify: {
        // id: "",
        // vip: "",
        description: "",
      },
      search: "",
      inventorys: [],
      timer: null,
      // radio: "",
    };
  },
  created() {
    this.get_inventory();
    this.timer = setInterval(() => {
      this.get_inventory();
    }, 30000);
  },
  beforeDestroy() {
    if (this.timer) {
      //如果定时器还在运行，直接关闭，不用判断
      clearInterval(this.timer); //关闭
    }
  },
  methods: {
    get_inventory() {
      this.$http
        .post("/api/add_redis/get_inventory/")
        .then((res) => {
          if (res.data.status === true) {
            // this.$message.success(res.data.msg);
            this.inventorys = res.data.data;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    handleEdit(index, row) {
      this.dialogdata_modify = row;
      this.dialogFormVisible_modify = true;
    },
    linkUpdate(row) {
      this.$router.push({
        path: "/home/redis/redis_detail",
        query: { ip: row.ip, description: row.description },
      });
    },
    save_inventory() {
      this.fullscreenLoading = true;
      setTimeout(() => {
        this.fullscreenLoading = false;
      }, 2000);
      this.postdata = {
        ip: this.dialogdata.ip,
        description: this.dialogdata.description,
        port: this.dialogdata.port,
        buffer_pool_size: this.dialogdata.buffer_pool_size,
        pwd: this.dialogdata.pwd,
      };
      this.$http
        .post("/api/add_redis/install_redis/", this.postdata)
        .then((res) => {
          if (res.data.status === true) {
            this.dialogFormVisible = false;
            console.log(res);
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

    modify_rds() {
      this.fullscreenLoading = true;
      setTimeout(() => {
        this.fullscreenLoading = false;
      }, 2000);
      this.postdata = {
        ip: this.dialogdata_modify.ip,
        description: this.dialogdata_modify.description,
      };
      this.$http
        .post("/api/add_redis/modify_rds/", this.postdata)
        .then((res) => {
          if (res.data.status === true) {
            this.dialogFormVisible_modify = false;
            console.log(res);
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
    handleDelete(index, row) {
      this.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.postdata = {
            // id: row.id,
            ip: row.ip,
          };
          this.$http
            .post("/api/add_redis/delete_inventory/", this.postdata)
            .then((res) => {
              if (res.data.status === true) {
                console.log(res);
                this.$message.success(res.data.msg);
                this.inventorys = res.data.data;
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
