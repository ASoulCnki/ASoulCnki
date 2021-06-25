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
  methods: {
    time_format(time) {
      var now = new Date();
      var time_num = parseInt(time) * 1000;
      now.setTime(time_num);
      return now.format("yyyy-MM-dd hh:mm:ss");
    },
  },
});

var clipboard = new ClipboardJS("#copy_result_btn", {
  text: function (trigger) {
    //标题
    var data_copyright = "枝网文本复制检测报告(简洁)\n";
    var data_time = "查重时间:" + info_head.time + "\n";
    //复制比
    var rate = info_head.rate;
    var data_rate = "总文字复制比:" + rate + "%\n";
    var related_list = JSON.parse(localStorage.getItem("related"));
    var data_related = "";
    if (related_list.length > 0) {
      data_related =
        "相似小作文:\n" +
        related_list[0][2] +
        "\n" +
        "作者:" +
        related_list[0][1].m_name +
        "\n";
    }
    //评价
    var comment = "我的评价是:";
    if (rate < 40.0) {
      comment += "原创/偷🥰\n";
    } else if (rate < 70.0) {
      comment += "有抄袭嫌疑🤨\n";
    } else {
      comment += "一眼偷🥵\n";
    }
    var copy_data =
      data_copyright + data_time + data_rate + data_related + comment;
    return copy_data;
  },
});
clipboard.on("success", function (e) {
  console.log(e);
  alert("复制成功");
});
clipboard.on("error", function (e) {
  console.log(e);
  alert("复制失败，请手动复制");
});
history.pushState(null, null, document.URL);
window.addEventListener("popstate", function () {
  window.location = "/";
});
