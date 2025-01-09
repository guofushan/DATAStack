<template>
  <div>
    <hr />
    <el-table
      :data="
        inventorys.filter(
          (data) =>
            !search || data.table_name.toLowerCase().includes(search.toLowerCase())
        )
      "
      style="width: 100%"
      height="800"
    >
      <el-table-column width="100">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.$index, scope.row)"
            >编辑</el-button
          >
        </template>
      </el-table-column>
      <el-table-column label="序列" width="60" type="index"> </el-table-column>
      <el-table-column label="任务名称" width="150" prop="comment"> </el-table-column>
      <el-table-column label="crontab" width="100" prop="cron"> </el-table-column>
      <el-table-column label="状态" width="80" prop="failed">
        <template slot-scope="scope">
          <el-tag :type="scope.row.failed == '成功' ? 'success' : 'warning'">
            {{ scope.row.failed }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="最后执行" width="100" prop="last_run"> </el-table-column>
      <el-table-column label="下次执行" width="100" prop="next_exec_time">
      </el-table-column>
    </el-table>
    <el-dialog title="详情" :visible.sync="dialogFormVisible" width="30%" center>
      <el-form :model="dialogdata" label-position="left" label-width="80px">
        <el-form-item label="crontab">
          <el-input
            v-model="dialogdata.cron"
            autocomplete="off"
            placeholder="例: 01 09 * * *"
          ></el-input>
        </el-form-item>
        <el-form-item label="command">
          <el-input
            v-model="dialogdata.command"
            autocomplete="off"
            placeholder="例: /usr/bin/python /tmp/test.py"
          ></el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="dialogdata.comment"
            autocomplete="off"
            placeholder="描述任务功能作用"
          ></el-input>
        </el-form-item>
        <el-form-item label="脚本IP">
          <el-input
            v-model="dialogdata.ip"
            autocomplete="off"
            placeholder="执行服务器IP"
          ></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-input
            v-model="dialogdata.failed"
            autocomplete="off"
            placeholder="禁填(自动赋值)"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="save_crontab">确 定</el-button>
        <el-button @click="dialogFormVisible = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialogFormVisible: false,
      dialogdata: {
        id: "",
        cron: "",
        command: "",
        comment: "",
        ip: "",
        failed: "",
      },
      search: "",
      inventorys: [],
      log: "",
    };
  },
  created() {
    this.get_crontab();
  },
  methods: {
    get_crontab() {
      this.$http
        .post("/api/mysql_crontab/get_crontab/")
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
    },

    save_crontab() {
      this.postdata = {
        cron: this.dialogdata.cron,
        command: this.dialogdata.command,
        comment: this.dialogdata.comment,
        ip: this.dialogdata.ip,
        id: this.dialogdata.id,
        failed: this.dialogdata.failed,
      };
      this.$http
        .post("/api/mysql_crontab/save_crontab/", this.postdata)
        .then((res) => {
          if (res.data.status === false) {
            this.$message.error(res.data.msg);
          } else {
            this.dialogFormVisible = false;
            this.$message.success(res.data.msg);
            this.inventorys = res.data.data;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    handleEdit(index, row) {
      this.dialogdata = row;
      this.dialogFormVisible = true;
    },

    handleDelete(index, row) {
      this.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.postdata = {
            id: row.id,
          };
          this.$http
            .post("/api/mysql_crontab/delete_crontab/", this.postdata)
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
