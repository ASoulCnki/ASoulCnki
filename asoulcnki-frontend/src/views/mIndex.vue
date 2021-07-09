<template>
  <div>
    <div id="main_form">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h3 class="panel-title">小作文</h3>
        </div>
        <div class="panel-body">
          <textarea
            class="form-control"
            rows="10"
            placeholder="内容字数不少于10个字，不多于1000字。输入信息后，点击下方「提交小作文」进行查重 !"
            v-model="text"
          ></textarea>
          <div id="agree_check">
            <input
              type="checkbox"
              v-model="agree_check"
              @click="agree_check_click"
            />
            我已同意<a href="/protocol" target="_blank"
              >《枝网查重平台用户协议》</a
            >
          </div>
        </div>
      </div>
      <div id="submit_btn_div">
        <div
          type="button"
          :class="button_class"
          @click="button_click"
          id="submit_btn"
        >
          {{ button_content }}
        </div>
      </div>
    </div>
    <div class="panel panel-default" id="introduction">
      <div class="panel-heading">
        <h3 class="panel-title">枝网查重系统介绍</h3>
      </div>
      <div class="panel-body">
        <p><b>比对库范围：</b><br />b站动态、视频评论区</p>
        <p>
          <b>检测算法：</b><br />
          [1]李旭.基于串匹配方法的文档复制检测系统研究[D]. 燕山大学.
        </p>
        <p><b>检测语种：</b><br />中文、英文、emoji</p>
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
        <span>
          <b>反馈地址：</b><br />
          <em
            ><a
              href="https://t.bilibili.com/542031663106174238"
              target="_blank"
              style="color: #4f6ef2"
              >ASoulCnki_Official</a
            ></em
          >
        </span>
      </div>
    </div>
    <ul class="list-group" id="asoul_link">
      <a
        class="list-group-item"
        :href="person.href"
        :key="person.href"
        target="_blank"
        v-for="person in person_list"
        >{{ person.name }}</a
      >
    </ul>
  </div>
</template>

<script>
import axios from "axios";
var post_url = "https://asoulcnki.asia/v1/api/check";
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
export default {
  data() {
    return {
      text: "",
      agree_check: true,
      maxlength: 1000,
      button_content: "提交小作文",
      button_class: "btn btn-info btn-lg",
      wait_result: false,
      person_list,
    };
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
              } else {
                alert("服务器返回错误");
              }
            })
            .catch((error) => {
              // 请求失败处理
              this.button_content = "提交小作文";
              this.button_class = "btn btn-info btn-lg";
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
@import url("../globalCSS/m_main.css");
</style>