<script setup lang="ts">
import { ref } from 'vue';

  const text = ref({
    name: '张三',
    age: 18,
    url: 'https://www.baidu.com',
    linkText: '百度'
  });
  function changeText() {
    text.value.name = '李四';
    text.value.age = 20;
    text.value.url = 'https://www.google.com';
    text.value.linkText = '谷歌';
  }
</script>

<template>
  <h1>
    {{ text.name }} - {{ text.age }}
    <div><a :href="text.url">{{ text.linkText }}</a></div>
  </h1>
  <button @click="changeText">Change Text</button>
</template>

<style>

</style>
