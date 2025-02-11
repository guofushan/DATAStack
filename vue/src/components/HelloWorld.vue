<template>
  <div>
    <el-row type="flex" justify="center" style="margin-top: 250px">
      <!-- <h1>DATAStack数据库私有云</h1> -->
      <h1>DATAStack</h1>
    </el-row>
    <el-row type="flex" justify="center" style="">
      <el-col :span="6">
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="用户名">
            <el-input v-model="form.username"></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input
              type="password"
              v-model="form.password"
              @keyup.enter.native="login"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="login">登录</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
    };
  },

  methods: {
    login: function () {
      this.postData = {
        username: this.form.username,
        password: this.$md5(this.form.password),
      };
      this.$http.post("/api/login", this.postData).then((res) => {
        if (res.data.status === true) {
          console.log(res);
          this.$message.success(res.data.msg);
          //全局存储token
          window.localStorage["token"] = JSON.stringify(res.data.data.token);
          this.$router.push("/home/mysql_instance");
        } else {
          this.$message.error(res.data.msg);
        }
      });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-row {
  margin-bottom: 20px;
}
</style>
