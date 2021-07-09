<template>
  <div>
    <div id="body_content">
      <div>
        <div id="pagecontent">
          <div class="content_left">
            <div id="main_form">
              <div class="form_item form_item_text">
                <div class="form_label"><i class="red">*</i>小作文</div>
                <div class="form_upload">
                  <div class="form_paste_wrapper" style="display: block">
                    <textarea
                      name="paper_text1"
                      placeholder="内容字数不少于10个字，不多于1000字。输入信息后，点击下方「提交小作文」进行查重 !"
                      :maxlength="maxlength"
                      v-model="text"
                    ></textarea>
                    <p>
                      <span class="form_paste_count"
                        ><em style="color: rgb(153, 153, 153)">{{
                          text.length
                        }}</em
                        >/{{ maxlength }}
                      </span>
                    </p>
                  </div>
                </div>
              </div>
              <div style="text-align: center">
                <div class="agree_check">
                  <input
                    id="paper_protocol_check"
                    type="checkbox"
                    v-model="agree_check"
                    @click="agree_check_click"
                  />
                  <span>我已同意</span>
                  <span>
                    <a
                      href="/protocol"
                      target="_blank"
                      style="color: #4f6ef2"
                      >《枝网查重平台用户协议》</a
                    >
                  </span>
                </div>
                <span :class="button_class" @click="button_click">
                  <span>{{ button_content }}</span>
                </span>
              </div>
            </div>
          </div>
          <div class="content_right">
            <div class="content_right_brand">
              <div class="right_top">枝网查重系统介绍</div>
              <div class="right_mid">
                <p>
                  <b>比对库范围：</b><br />
                  <em>b站动态、视频评论区</em>
                </p>
                <p>
                  <b>检测算法：</b><br />
                  <em
                    >[1]李旭.基于串匹配方法的文档复制检测系统研究[D].
                    燕山大学.</em
                  >
                </p>
                <p><b>检测语种：</b><br /><em>中文、英文、emoji</em></p>
                <p>
                  <b>开源地址：</b><br />
                  <em
                    ><a
                      href="https://github.com/stream2000/ASoulCnki"
                      target="_blank"
                      style="color: #4f6ef2"
                      >ASoulCnki</a
                    ></em
                  >
                </p>
                <p>
                  <b>反馈地址：</b><br />
                  <em
                    ><a
                      href="https://t.bilibili.com/542031663106174238"
                      target="_blank"
                      style="color: #4f6ef2"
                      >ASoulCnki_Official</a
                    ></em
                  >
                </p>
              </div>
              <div class="right_bottom" id="asoul_link">
                <p v-for="person in person_list" :key="person.name">
                  <a
                    :href="person.href"
                    style="color: rgb(251, 114, 153)"
                    target="_blank"
                    >{{ person.name }}</a
                  >
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
var post_url = "https://asoulcnki.asia/v1/api/check";
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
const person_list = [
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
];

export default {
  name: "Home",
  data() {
    return {
      text: "",
      agree_check: true,
      maxlength: 1000,
      button_content: "提交小作文",
      button_class: "submit_btn",
      wait_result: false,
      person_list,
    };
  },
  mounted() {
    try {
      console.log(navigator.userAgent);
      if (navigator.userAgent.match(/(iPhone|iPod|Android|ios|iPad)/i)) {
        window.location = "m_index";
      }
    } catch (err) {}
  },
  methods: {
    button_click() {
      if (this.text.length < 10) {
        alert("小作文字数太少了哦~");
        return;
      }
      if (this.agree_check) {
        if (!this.wait_result) {
          this.button_content = "查重中...";
          this.button_class = "submit_btn_clicked";
          this.wait_result = true;
          localStorage.setItem("text", this.text);
          axios
            .post(post_url, { text: this.text })
            .then((response) => {
              this.button_content = "提交小作文";
              this.button_class = "submit_btn";
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
              } else {
                alert("服务器返回错误");
              }
            })
            .catch((error) => {
              // 请求失败处理
              this.button_content = "提交小作文";
              this.button_class = "submit_btn";
              this.wait_result = false;
              alert(error);
              console.log(error);
            });
        }
      } else {
        alert("您未同意《枝网查重平台用户协议》");
      }
    },
    agree_check_click() {
      this.agree_check = !this.agree_check;
    },
  },
};
</script>

<style>
@import url("../globalCSS/main.css");
</style>