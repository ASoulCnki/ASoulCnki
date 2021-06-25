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
var src_text = new Vue({
  el: "#src_text",
  data: {},
  computed: {
    text: function () {
      return localStorage.getItem("text");
    },
  },
});
var info_head = new Vue({
  el: "#info_head",
  data: {
    han_length: 0,
    eng_length: 0,
    num_length: 0,
    time: "",
    start_time: "",
    end_time: "",
    rate: 0,
    progress_class: "progress-bar",
    rate_color: "",
  },
  created: function () {
    var text = localStorage.getItem("text").replace("\n", "").replace(" ", "");
    var han = text.match(/[^ -~]/g);
    var eng = text.match(/[a-z]/gi);
    var num = text.match(/\d/g);
    if (han) {
      this.han_length = han.length;
    }
    if (eng) {
      this.eng_length = eng.length;
    }
    if (num) {
      this.num_length = num.length;
    }
    this.time = localStorage.getItem("time");
    this.start_time = localStorage.getItem("start_time");
    this.end_time = localStorage.getItem("end_time");
    var rate = localStorage.getItem("rate") * 100;
    this.rate = rate.toFixed(2);
    if (rate < 20) {
      this.progress_class = "progress-bar progress-bar-success";
      this.rate_color = "green";
    } else if (rate < 60) {
      this.progress_class = "progress-bar progress-bar-warning";
      this.rate_color = "orange";
    } else {
      this.progress_class = "progress-bar progress-bar-danger";
      this.rate_color = "red";
    }
  },
});

var related = new Vue({
  el: "#related",
  data: {
    related_list: [],
  },
  created: function () {
    this.related_list = JSON.parse(localStorage.getItem("related"));
  },
  filters: {
    rounding(value) {
      return value.toFixed(2);
    },
  },
  methods:{
    time_format(time){
      var now = new Date();
      var time_num = parseInt(time) * 1000
      now.setTime(time_num);
      return now.format("yyyy-MM-dd hh:mm:ss")
    }
  }
});
history.pushState(null, null, document.URL);
window.addEventListener("popstate", function () {
  window.location = "/";
});
