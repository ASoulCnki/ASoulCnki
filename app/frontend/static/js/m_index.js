var post_url = "/v1/api/check";
Date.prototype.format = function (fmt) {
  var o = {
    "M+": this.getMonth() + 1, //月份
    "d+": this.getDate(), //日
    "h+": this.getHours(), //小时
    "m+": this.getMinutes(), //分
    "s+": this.getSeconds(), //秒
    "q+": Math.floor((this.getMonth() + 3) / 3), //季度
    S: this.getMilliseconds(), //毫秒
  };
  if (/(y+)/i.test(fmt)) {
    fmt = fmt.replace(
      RegExp.$1,
      (this.getFullYear() + "").substr(4 - RegExp.$1.length)
    );
  }
  for (var k in o) {
    if (new RegExp("(" + k + ")", "i").test(fmt)) {
      fmt = fmt.replace(
        RegExp.$1,
        RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length)
      );
    }
  }
  return fmt;
};
var main_form = new Vue({
  el: "#main_form",
  data: {
    text: "",
    agree_check: true,
    maxlength: 1000,
    button_content: "提交小作文",
    button_class: "btn btn-info btn-lg",
    wait_result: false,
  },
  methods: {
    button_click() {
      if (this.agree_check) {
        if (!this.wait_result && this.text.length >= 10) {
          this.button_content = "查重中...";
          this.button_class = "btn btn-info btn-lg disabled";
          this.wait_result = true;
          localStorage.setItem("text", this.text);
          axios
            .post(post_url, { text: this.text })
            .then((response) => {
              this.button_content = "提交小作文";
              this.button_class = "btn btn-info btn-lg";
              this.wait_result = false;
              if (response.data.code == 0) {
                //时间设置
                var now = new Date();
                var nowStr = now.format("yyyy-MM-dd hh:mm:ss");
                localStorage.setItem("time", nowStr);
                var start_time = parseInt(response.data.data.start_time) * 1000;
                var end_time = parseInt(response.data.data.end_time) * 1000;
                now.setTime(start_time);
                localStorage.setItem("start_time", now.format("yyyy-MM-dd"));
                now.setTime(end_time);
                localStorage.setItem("end_time", now.format("yyyy-MM-dd"));
                //查重率
                localStorage.setItem("rate", response.data.data.rate);
                //相似小作文
                localStorage.setItem(
                  "related",
                  JSON.stringify(response.data.data.related)
                );
                //跳转
                window.location.href = "/result";
              }
            })
            .catch(function (error) {
              // 请求失败处理
              console.log(error);
            });
        }
      }
      if (this.text.length < 10) {
        alert("小作文字数太少了哦~");
      } else {
        alert("您未同意《枝网查重平台用户协议》");
      }
    },
    agree_check_click() {
      this.agree_check = !this.agree_check;
    },
  },
});
var asoul_link = new Vue({
  el: "#asoul_link",
  data: {
    person_list: [
      {
        name: "A-SOUL_Official",
        href: "https://space.bilibili.com/703007996/",
      },
      {
        name: "贝拉kira",
        href: "https://space.bilibili.com/672353429/",
      },
      {
        name: "嘉然今天吃什么",
        href: "https://space.bilibili.com/672328094/",
      },
      {
        name: "向晚大魔王",
        href: "https://space.bilibili.com/672346917/",
      },
      {
        name: "乃琳Queen",
        href: "https://space.bilibili.com/672342685/",
      },
      {
        name: "珈乐Carol",
        href: "https://space.bilibili.com/351609538/",
      },
    ],
  },
});
