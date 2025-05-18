<script setup lang="ts">
import {RouterView} from "vue-router";

//useRoute表示接受路由信息的函数
import {useRoute} from "vue-router";
let route = useRoute();
let msg=route.query.msg;//通过query传参



</script>

<template>
  A组件
  <router-link to="/gn">国内</router-link>-
  <router-link to="/gj">国际</router-link>
  <div style="width: 200px;height: 50px; border: 1px solid red">
    <router-view></router-view>
  </div>
</template>

<style scoped>

</style>