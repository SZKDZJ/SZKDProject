<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import login from './views/login.vue';
import {ref} from "vue";

let mymsg=ref()
</script>

  <!--模版 div-->
<template>

<!--  &lt;!&ndash;指定login组件位置&ndash;&gt;-->
<!--  <login></login>-->

  <!--路由跳转-->
  <!--1.  需要多个组件-->
  <!--2. 路由页面 配置 地址与组件 对应关系-->
  <!--3. 调用 路由地址-->
  <!--4. 组件出口-->
  <!--<router-link to="/a">链接A组件</router-link>-->
  <!--路由传参-->
  <!--<router-link to="/a?msg=4010">链接A组件</router-link>-->
  <!--传递动态变量-->
  <input type="text" v-model="mymsg" /> <br/>
  <router-link :to="'/a?msg'+mymsg">链接A组件</router-link>


  <div style="width: 300px;height: 100px; border: 1px solid red">
    <router-view></router-view>
  </div>


</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
