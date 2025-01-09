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
      <el-table-column width="180">
        <template slot="header">
          <el-button
            type="primary"
            icon="el-icon-plus"
            size="large"
            :style="{ float: 'left' }"
            @click="
              dialogFormVisible = true;
              dialogdata = {
                id: '',
                url: '',
                user: '',
                pwd: '',
                description: '',
              };
            "
            >新增</el-button
          >
        </template>
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.$index, scope.row)"
            >编辑</el-button
          >
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>

      <el-table-column label="访问链接" width="200" show-overflow-tooltip>
        <template slot-scope="scope">
          <a :href="scope.row.url" target="_blank" class="buttonText">{{
            scope.row.description
          }}</a>
        </template>
      </el-table-column>

      <el-table-column label="用户" width="100" prop="user"> </el-table-column>
      <el-table-column label="密码" prop="pwd" show-overflow-tooltip="true">
      </el-table-column>
    </el-table>
    <el-dialog title="详情" :visible.sync="dialogFormVisible" width="30%" center>
      <el-form :model="dialogdata" label-position="left" label-width="80px">
        <el-form-item label="访问链接">
          <el-input
            v-model="dialogdata.url"
            autocomplete="off"
            placeholder="例: http://192.168.1.1:3000"
          ></el-input>
        </el-form-item>
        <el-form-item label="用户">
          <el-input v-model="dialogdata.user" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="dialogdata.pwd" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="dialogdata.description"
            autocomplete="off"
            placeholder="描述平台作用功能"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="save_inventory">确 定</el-button>
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
        url: "",
        user: "",
        pwd: "",
        description: "",
      },
      search: "",
      inventorys: [],
    };
  },
  created() {
    this.get_inventory();
  },
  methods: {
    get_inventory() {
      this.$http
        .post("/api/yunweicenter/get_inventory/")
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
    handleEdit(index, row) {
      this.dialogdata = row;
      this.dialogFormVisible = true;
    },
    save_inventory() {
      this.postdata = {
        id: this.dialogdata.id,
        url: this.dialogdata.url,
        user: this.dialogdata.user,
        pwd: this.dialogdata.pwd,
        description: this.dialogdata.description,
      };
      this.$http
        .post("/api/yunweicenter/save_inventory/", this.postdata)
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
            .post("/api/yunweicenter/delete_inventory/", this.postdata)
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
