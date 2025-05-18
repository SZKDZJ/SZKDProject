<!--只用在App.vue中写，不要在html中写，app会对应过去-->

<!--template 表示一段html代码，可以理解为一个大的div-->
<template>
  <!--  绑定{{}} 和变量  -->
  大家好，{{msg}} --- {{age}}+2
  <br/><input type="text" v-model="msg" />
  <button @click="btn">修改数据</button><br />

  <!-- : 绑定属性和变量   -->
  <a :href="path">链接网站</a>
  <br><button type="button" @click="baidu">链接百度</button>
  <br><button type="button" @click="wangyi">链接163</button>
  <br/>

  <!--图片-->
  <img width="300px" :src="pathing" alt=" "/>
  <br><button type="button" @click="shaqiu1">链接1</button>
  <br><button type="button" @click="shaqiu2">链接2</button>

  <!--
  <br><h1>作业</h1>
  <br><div>
    <ul>
      <li>足球</li>
      <li>篮球</li>
      <li>羽毛球</li>
    </ul>
  </div>-->

  <!--条件渲染：满足条件才会显示-->
  <br>
  <input >
  <h2 v-if="age<25">年轻</h2>
  <h2 v-else-if="age<40"></h2>
  <h2 v-else>年老</h2>

  <ul>
    <li v-for="item in student">{{item}}</li>
  </ul>



</template>

<!--是针对html代码进行的逻辑处理-->
<script setup lang="ts">
  import {ref} from "vue";

  //响应式，将input响应到msg；v-model双向绑定
  let msg=ref("困");
  let age=23;
  function btn(){
    alert("click")
    //console.log(msg)
    msg.value="饿"//注意：.value 修改会响应在页面上
  }

  let path=ref("http://www.baidu.com")
  function baidu(){
    path.value="http://www.baidu.com"
  }
  function wangyi(){
    path.value="http://www.163.com"
  }

  let pathing=ref("http://img2.baidu.com/it/u=2157803387,2579025484&fm=253&app=138&f=JPEG?w=800&h=1067")
  function shaqiu1(){
    pathing.value="http://img2.baidu.com/it/u=2157803387,2579025484&fm=253&app=138&f=JPEG?w=800&h=1067"
  }
  function shaqiu2(){
    pathing.value="https://img0.baidu.com/it/u=833888250,756230357&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=1067"
  }

  let student = ref(['Marry','Helen','Tim'])

</script>

<!--针对html的样式处理，scoped（表示只针对这段html代码起作用）-->
<style scoped>
  h1{
    color: #4c4ce5;
  }
</style>
