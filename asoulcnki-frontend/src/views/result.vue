<template>
  <div class="panel panel-default" id="panel">
    <div class="panel-body">
      <div id="title">
        <h3><b>文本复制检测报告单(枝网)</b></h3>
      </div>
      <div class="head" id="info_head">
        <p class="time"><span class="head_li">检测时间：</span>{{ time }}</p>
        <p class="detection_range">
          <span class="head_li"> 检测范围：</span>b站评论
        </p>
        <p class="time_range">
          <span class="head_li"> 时间范围：</span>{{ start_time }}至{{
            end_time
          }}
        </p>
        <p class="length">
          <span class="head_li">字数：</span>
          {{ han_length }}个汉字 {{ eng_length }}个英文 {{ num_length }}个数字
        </p>
        <p class="detection_range">
          <b :style="'color: ' + rate_color + '; font-size: medium'">
            总文字复制比：{{ rate }}%</b
          >
        </p>
        <div class="progress">
          <div
            :class="progress_class"
            role="progressbar"
            :aria-valuenow="rate"
            aria-valuemin="0"
            aria-valuemax="100"
            :style="'width:' + rate + '%;'"
          >
            <span class="sr-only"></span>
          </div>
        </div>
      </div>
      <div class="result_body">
        <div id="copy_result">
          <button type="button" class="btn btn-info" id="copy_result_btn">
            复制查重结果
          </button>
          <p>
            查重结果仅作参考，请注意辨别是否为原创<br />(算法更新中,不足之处欢迎<a
              href="https://t.bilibili.com/542031663106174238"
              target="_blank"
              >点此反馈</a
            >)
          </p>
        </div>
        <p class="result_title">原文</p>
        <div class="result_box">
          <div class="result_box_inner">
            <div id="src_text" style="word-wrap: break-word">
              <p>{{ text }}</p>
            </div>
          </div>
        </div>
        <p class="result_title" style="margin-top: 20px">相似小作文</p>
        <div id="related">
          <div v-for="essay in related_list" :key="essay.ctime">
            <div style="width: 80%; margin: auto">
              <div class="result_box_inner">
                <div style="margin: 20px">
                  <div class="row">
                    <div class="col-md-6">
                      <p style="margin: 0px">
                        <span style="color: rgb(23, 121, 204)">作者：</span
                        >{{ essay[1].m_name }}
                      </p>
                      <p style="margin: 0px">
                        <span style="color: rgb(23, 121, 204)">发表时间：</span
                        >{{ time_format(essay[1].ctime) }}
                      </p>
                      <p style="margin: 0px">
                        <span style="color: rgb(23, 121, 204)">相似率：</span
                        >{{ (essay[0] * 100) | rounding }}%
                      </p>
                      <p>
                        <a :href="essay[2]" target="_blank">查看原文</a>
                      </p>
                    </div>
                    <div class="col-md-6">
                      <p style="margin: 0px">
                        <span
                          style="white-space: pre-wrap; word-wrap: break-word"
                          class="related_content"
                          >{{ essay[1].content }}</span
                        >
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div style="margin-bottom: 40px"></div>
    </div>
  </div>
</template>

<script>
function time_format(time) {
  var now = new Date();
  var time_num = parseInt(time) * 1000;
  now.setTime(time_num);
  return now.format("yyyy-MM-dd hh:mm:ss");
}
export default {
  data() {
    return {
      han_length: 0,
      eng_length: 0,
      num_length: 0,
      time: "",
      start_time: "",
      end_time: "",
      rate: 0,
      progress_class: "progress-bar",
      rate_color: "",
      related_list: [],
    };
  },
  created() {
    // set title
    document.title = "枝网检测报告";
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
    this.related_list = JSON.parse(localStorage.getItem("related"));
  },
  mounted: function () {
    //保证加载完成后再处理(用v-html可能发生xss)
    this.$nextTick(function () {
      var sanitizeHTML = function (str) {
        //处理字符串内容防止xss
        var temp = document.createElement("div");
        temp.textContent = str;
        return temp.innerHTML;
      };
      var sensitive_len = 4; //敏感的长度
      var all_text = ""; //所有相关文章拼接起来
      var related_text_list =
        document.getElementsByClassName("related_content");
      var src_text_element = document.getElementById("src_text");
      var src_text = localStorage.getItem("text");
      var src_text_result = sanitizeHTML(src_text);
      for (i = 0; i < related_text_list.length; i++) {
        related_text_element = related_text_list[i];
        related_text = sanitizeHTML(related_text_element.innerHTML);
        var result_text = related_text;
        all_text += related_text;
        for (j = 0; j < related_text.length; ) {
          var dis = 0;
          var search_text = related_text.substr(j, sensitive_len + dis);
          while (src_text.indexOf(search_text) != -1) {
            dis += 1;
            search_text = related_text.substr(j, sensitive_len + dis);
            if (j + sensitive_len + dis > related_text.length) {
              break;
            }
          }
          if (
            src_text.indexOf(related_text.substr(j, sensitive_len + dis - 1)) !=
            -1
          ) {
            var reg = new RegExp(
              related_text.substr(j, sensitive_len + dis - 1),
              "g"
            );
            result_text = result_text.replace(
              reg,
              "<span style='color:red'>" +
                sanitizeHTML(related_text.substr(j, sensitive_len + dis - 1)) +
                "</span>"
            );
            console.log(result_text);
          }
          j = j + dis + sensitive_len - 1;
        }
        related_text_element.innerHTML = result_text;
      }
      for (j = 0; j < src_text.length; ) {
        var dis = 0;
        search_text = src_text.substr(j, sensitive_len + dis);
        if (j + sensitive_len + dis >= src_text.length) {
          break;
        }
        while (all_text.indexOf(search_text) != -1) {
          dis += 1;
          search_text = src_text.substr(j, sensitive_len + dis);
          if (j + sensitive_len + dis > src_text.length) {
            break;
          }
        }
        if (
          all_text.indexOf(src_text.substr(j, sensitive_len + dis - 1)) != -1
        ) {
          var reg = new RegExp(
            src_text.substr(j, sensitive_len + dis - 1),
            "g"
          );
          src_text_result = src_text_result.replace(
            reg,
            "<span style='color:red'>" +
              sanitizeHTML(src_text.substr(j, sensitive_len + dis - 1)) +
              "</span>"
          );
        }
        j = j + dis + sensitive_len - 1;
      }
      src_text_element.innerHTML = src_text_result;
    });
  },
  filters: {
    rounding(value) {
      return value.toFixed(2);
    },
  },
  computed: {
    text() {
      return localStorage.getItem("text");
    },
  },
  methods: {
    time_format,
  },
};
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
        "\n" +
        "发表时间:" +
        time_format(related_list[0][1].ctime) +
        "\n";
    }
    //评价
    // var comment = "我的评价是:";
    // if (rate < 40.0) {
    //   comment += "原创/偷🥰\n";
    // } else if (rate < 70.0) {
    //   comment += "有抄袭嫌疑🤨\n";
    // } else {
    //   comment += "一眼偷🥵\n";
    // }
    var notice = "\n查重结果仅作参考，请注意辨别是否为原创";
    var copy_data =
      data_copyright + data_time + data_rate + data_related + notice;
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
</script>

<style>
body {
  background: #ebebeb;
}
#panel {
  width: 90%;
  margin: auto;
  margin-top: 20px;
}
#title {
  margin-bottom: 20px;
}
#title h3 {
  text-align: center;
}
#info_head {
  margin: 10px;
  margin-left: 20px;
}
.head_li {
  color: rgb(23, 121, 204);
}
.result_title {
  text-align: center;
  font-size: medium;
  font-weight: 1000;
  color: rgb(23, 121, 204);
}
.result_box {
  width: 80%;
  margin: auto;
}
.result_box_inner {
  margin: 10px;
  border-radius: 10px;
  border: 1px solid #e2e0e0;
}
.result_box_inner #src_text {
  margin: 20px;
  white-space: pre-wrap;
}
#copy_result {
  text-align: center;
}

#copy_result .btn {
  margin: 20px;
}
</style>