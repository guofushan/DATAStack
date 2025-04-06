<template>
  <div>
    <el-form label-position="left" label-width="120px">
      <el-button
        size="medium"
        type="primary"
        icon="el-icon-circle-plus"
        @click="handleEdit()"
        round
        >创建数据库</el-button
      >
      <el-divider></el-divider>
    </el-form>

    <el-table :data="db_lists" style="width: 100%" border height="800">
      <el-table-column label="数据库名称" width="150" prop="schema_name">
      </el-table-column>
      <el-table-column label="字符集" width="150" prop="DEFAULT_CHARACTER_SET_NAME">
      </el-table-column>
      <el-table-column label="绑定账号" prop="grant_users"> </el-table-column>
    </el-table>

    <el-dialog title="创建数据库" :visible.sync="dialogFormVisible" width="30%" center>
      <el-form :model="dialogdata" label-position="left" label-width="120px">
        <el-form-item label="数据库(DB)名称">
          <el-input v-model="dialogdata.dbname" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="save_db">确 定</el-button>
        <el-button @click="dialogFormVisible = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      db_lists: [],
      dialogFormVisible: false,
      dialogdata: {
        dbname: "",
      },
      vip: "",
    };
  },
  created: function () {
    this.get_dbinfo();
  },
  methods: {
    get_dbinfo() {
      this.vip = this.$route.query.vip;
      this.$http
        .post("/api/mysql_dbcreate/get_dbinfo/", {
          vip: this.vip,
        })
        .then((res) => {
          if (res.data.status === true) {
            this.$message.success(res.data.msg);
            this.db_lists = res.data.data;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    handleEdit() {
      this.dialogFormVisible = true;
    },
    save_db() {
      this.vip = this.$route.query.vip;
      this.postdata = {
        dbname: this.dialogdata.dbname,
        vip: this.vip,
      };
      this.$http
        .post("/api/mysql_dbcreate/save_db/", this.postdata)
        .then((res) => {
          if (res.data.status === true) {
            this.dialogFormVisible = false;
            this.$message.success(res.data.msg);
            this.db_lists = res.data.data;
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

<style></style>
