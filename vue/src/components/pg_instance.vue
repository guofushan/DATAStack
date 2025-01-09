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
            <el-dropdown-menu slot="dropdown">
              <el-row>
                <el-button
                  type="warning"
                  icon="el-icon-plus"
                  size="small"
                  :style="{ float: 'left' }"
                  @click="
                    dialogFormVisible_2 = true;
                    dialogdata_2 = {
                      ip_one: '',
                      description: '',
                      ip_two: '',
                      bufpool: '',
                      db_version: '',
                    };
                  "
                  >高可用</el-button
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

      <el-table-column label="VIP" width="200" prop="vip" sortable> </el-table-column>
      <el-table-column label="端口" width="70" prop="port"> </el-table-column>
      <el-table-column label="创建时间" width="180" prop="date_created">
      </el-table-column>
      <el-table-column label="版本" width="120" prop="pg_version"> </el-table-column>
      <el-table-column label="IP地址" prop="ips"> </el-table-column>
    </el-table>

    <el-dialog title="高可用" :visible.sync="dialogFormVisible_2" width="30%" center>
      <el-form :model="dialogdata_2" label-position="left" label-width="80px">
        <el-form-item label="主库IP">
          <el-input v-model="dialogdata_2.ip_one" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="从库IP">
          <el-input v-model="dialogdata_2.ip_two" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="内存(GB)">
          <el-input
            v-model="dialogdata_2.bufpool"
            autocomplete="off"
            placeholder="shared_buffers(填写数字即可)"
          ></el-input>
        </el-form-item>
        <el-form-item label="RDS备注">
          <el-input
            v-model="dialogdata_2.description"
            autocomplete="off"
            placeholder="描述业务、用途"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="create_ha">确 定</el-button>
        <el-button @click="dialogFormVisible_2 = false">取 消</el-button>
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
      dialogFormVisible_2: false,
      dialogFormVisible_modify: false,
      dialogdata_2: {
        ip_one: "",
        ip_two: "",
        bufpool: "",
        description: "",
      },
      dialogdata_modify: {
        // id: "",
        vip: "",
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
      this.getinventory();
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
        .post("/api/pg_addinstance/get_inventory/")
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
    getinventory() {
      this.$http
        .post("/api/pg_addinstance/getinventory/")
        .then((res) => {
          if (res.data.status === true) {
            // this.$message.success(res.data.msg);
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
        path: "/home/mysql/mysql_detail",
        query: { vip: row.vip, description: row.description },
      });
    },
    create_ha() {
      setTimeout(() => {
        this.fullscreenLoading = false;
      }, 2000);
      this.postdata = {
        ip_one: this.dialogdata_2.ip_one,
        description: this.dialogdata_2.description,
        ip_two: this.dialogdata_2.ip_two,
        bufpool: this.dialogdata_2.bufpool,
        db_version: this.dialogdata_2.db_version,
      };
      this.fullscreenLoading = true;
      this.$http
        .post("/api/pg_addinstance/save_ha/", this.postdata)
        .then((res) => {
          if (res.data.status === true) {
            this.dialogFormVisible_2 = false;
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
        vip: this.dialogdata_modify.vip,
        description: this.dialogdata_modify.description,
      };
      this.$http
        .post("/api/pg_addinstance/modify_rds/", this.postdata)
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
            vip: row.vip,
            ips: row.ips,
          };
          this.$http
            .post("/api/pg_addinstance/delete_inventory/", this.postdata)
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
