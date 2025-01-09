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
      ip: "",
      iframeUrl: [],
    };
  },
  created: function () {
    this.get_inventory();
  },
  methods: {
    get_inventory() {
      this.ip = this.$route.query.ip;
      this.$http
        .post("/api/mysql_log/redis_granafa_ip/", { ip: this.ip })
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
