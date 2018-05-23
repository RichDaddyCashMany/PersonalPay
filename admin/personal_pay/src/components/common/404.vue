<template>
  <div class="container">
    <div class="wrap">
      <span>路径不存在！前往</span>
      <span class="link" @click="onclick('login')">登录</span>
      <span>/</span>
      <span class="link" @click="onclick('message')">管理台</span>
      <span>？</span>
    </div>
  </div>
</template>

<style scoped>
  div.container {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }
  div.wrap {
  }
  span {
    font-size: 40px;
    color: #333;
  }
  span.link {
    cursor: pointer;
    color: #409EFF;
  }
</style>

<script>
  export default {
    data () {
      return {
      }
    },
    methods: {
      onclick (value) {
        this.$router.push({
          name: value
        })
      }
    },
    created: function () {
    }
  }
</script>