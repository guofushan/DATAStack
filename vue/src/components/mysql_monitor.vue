<template>
  <div>
    <!-- <a
      href="http://10.88.28.3:3000/d/rYdddlPWk/linux?orgId=1&refresh=10s"
      target="showList"
      >显示内容</a
    > -->

    <iframe
      frameborder="0"
      :src="iframeUrl"
      width="100%"
      height="1000"
      scrolling="auto"
      style="background-color: transparent"
    >
    </iframe>
  </div>
</template>

<script>
export default {
  data() {
    return {
      vip: "",
      iframeUrl: [],
    };
  },
  created: function () {
    this.get_inventory();
  },
  methods: {
    get_inventory() {
      this.vip = this.$route.query.vip;
      this.$http
        .post("/api/mysql_log/granafa_ip/",{
          vip: this.vip,
        })
        .then((res) => {
          if (res.data.status === true) {
            this.$message.success(res.data.msg);
            this.iframeUrl = res.data.data;
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
