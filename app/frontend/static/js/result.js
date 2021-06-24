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
});
history.pushState(null, null, document.URL);
window.addEventListener("popstate", function () {
  window.location = "/";
});
