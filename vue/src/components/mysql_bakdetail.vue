<template>
  <div>
    <el-tabs type="border-card" v-model="activeName">
      <el-tab-pane label="数据备份" name="first">
        <hr />
        <el-table
          :data="
            inventorys.filter(
              (data) =>
                !search || data.command.toLowerCase().includes(search.toLowerCase())
            )
          "
          :row-class-name="jobtableRowClassName"
          border
          height="700"
        >
          <el-table-column label="备份节点" width="200" prop="ip"> </el-table-column>
          <el-table-column label="备份文件" width="350" prop="file_name">
          </el-table-column>
          <el-table-column label="备份大小" width="100" prop="file_size">
          </el-table-column>
          <el-table-column label="状态" width="100" prop="backup_status">
          </el-table-column>
          <el-table-column label="开始时间" width="180" prop="create_time">
          </el-table-column>
          <el-table-column label="结束时间" prop="update_time"> </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane
        :row-class-name="jobtableRowClassName"
        border
        height="700"
        label="备份设置"
        name="second"
      >
        <el-descriptions direction="horizontal" :column="1" :data="bakset_data">
          <template slot="title">
            <el-button
              type="primary"
              size="small"
              @click="
                dialogFormVisible = true;
                dialogdata = {
                  vip: '',
                  bak: '',
                  bak_store: '',
                };
              "
              >备份设置</el-button
            >

            <el-dialog :visible.sync="dialogFormVisible" title="备份设置">
              <el-form :model="dialogdata" label-position="left" label-width="150px">
                <el-form-item label="是否备份">
                  <el-input
                    v-model="dialogdata.bak"
                    autocomplete="off"
                    placeholder="是或否"
                  ></el-input>
                </el-form-item>
                <el-form-item label="数据备份保留天数">
                  <el-input
                    v-model="dialogdata.bak_store"
                    autocomplete="off"
                    placeholder="整型数字(默认5)"
                  ></el-input>
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="save_set">确 定</el-button>
              </span>
            </el-dialog>
          </template>

          <el-descriptions-item
            label="是否备份"
            v-for="item in bakset_data"
            :key="item.bak"
          >
            {{ item.bak }}
          </el-descriptions-item>

          <el-descriptions-item
            label="数据备份保留天数"
            v-for="item in bakset_data"
            :key="item.bak"
          >
            {{ item.bak_store }}
          </el-descriptions-item>
        </el-descriptions>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeName: "first",
      options: [],
      ip: "",
      detail_table: [],
      inventorys: [],
      bakset_data: [],
      dialogFormVisible: false,
      dialogdata: {
        vip: "",
        bak: "",
        bak_store: "",
      },
    };
  },
  created() {
    this.get_inventory();
    this.get_bakset();
  },
  methods: {
    get_inventory() {
      this.vip = this.$route.query.vip;
      this.$http
        .post("/api/mysql_backup/bak_detail/", {
          vip: this.vip,
        })
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
    get_bakset() {
      this.vip = this.$route.query.vip;
      this.$http
        .post("/api/mysql_backup/bak_set/", {
          vip: this.vip,
        })
        .then((res) => {
          if (res.data.status === true) {
            console.log(res);
            this.$message.success(res.data.msg);
            this.bakset_data = res.data.data;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    save_set() {
      this.vip = this.$route.query.vip;
      this.postdata = {
        bak: this.dialogdata.bak,
        bak_store: this.dialogdata.bak_store,
        vip: this.vip,
      };
      this.$http
        .post("/api/mysql_backup/save_set/", this.postdata)
        .then((res) => {
          if (res.data.status === false) {
            this.$message.error(res.data.msg);
          } else {
            this.dialogFormVisible = false;
            this.$message.success(res.data.msg);
            this.bakset_data = res.data.data;
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
