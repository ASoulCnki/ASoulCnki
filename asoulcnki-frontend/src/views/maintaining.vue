<template>
  <div class="main-style">
    <div class="no_data">
      <img class="no_dataImg" src="../assets/images/2.gif" alt="暂无数据" />
      <div class="no_dataText">
        系统维护中
        <p>
          为了AU们能获得更好的查重体验
          枝网将在2021年6月30日15:00-17:00进行维护。
        </p>
        <p>
          系统维护后将换用高性能java后端，采用最新国产分布式总线技术，预计快500%。不要问我们数据哪里来的（
        </p>
      </div>
      <!--<img class="width100" src="images/1.png" alt="底部">-->
    </div>
  </div>
</template>

<script>
export default {
  created() {
    document.title = "系统维护中";
  },
};
</script>

<style>
body,
a,
a:link {
  cursor: url("../assets/images/cur117.cur"), default;
}

a:hover {
  cursor: url("../assets/images/cur117.cur"), wait;
}
.no_data {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fafafa;
}
.no_dataText {
  text-align: center;
  padding: 0px 0px 90px 0px;
  color: #bebebe;
  font-size: 24px;
  font-weight: bold;
}
.no_dataImg {
  width: 240px;
  padding: 170px 0px 50px 0px;
}
</style>