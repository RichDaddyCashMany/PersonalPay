<template>
  <div class="container">
    <el-card>
      <div class="head">
        <img class="logo" src="../../images/logo.png">
      </div>
      <el-form :model="form" :rules="rules" ref="form" label-width="100px" class="form">
        <el-form-item label="账号" prop="username">
          <el-input v-model="form.username" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" auto-complete="off" type="password"></el-input>
        </el-form-item>
        <el-form-item class="button-container">
          <el-button type="primary" :loading="loginButtonLoading" @click="submitForm">登录</el-button>
          <el-button type="default" @click="onGotoReg">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
  import api from '../../util/api.js'

  export default {
    data () {
      return {
        loginButtonLoading: false,
        form: {
          username: '',
          password: ''
        },
        rules: {
          username: [
            { required: true, message: '请输入账号', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' }
          ]
        }
      }
    },
    methods: {
      submitForm () {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            localStorage.username = this.form.username
            this.requestLogin()
          } else {
            return false
          }
        })
      },
      onGotoReg () {
        this.$router.push({
          name: 'reg'
        })
      },
      requestLogin () {
        this.regButtonLoading = true

        api.login(this.form, (res) => {
          this.regButtonLoading = false

          if (res.status === 200) {
            const data = res.data
            if (data.code === 0) {
              this.$message('登录成功')
              this.$router.push({
                name: 'merchantDetail'
              })
            } else {
              this.$message(data.message)
            }
          } else {
            this.$message('请求超时')
          }
        })
      }
    },
    created: function () {
      this.form.username = localStorage.username
    }
  }
</script>

<style scoped>
  div.container {
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }
  .head {
    display: flex;
    justify-content: center;
    padding: 20px 0 20px 0;
  }
  .logo {
    height: 24px;
  }
  .form {
    width: 400px;
    padding: 20px 50px 20px 0;
  }
  .button-container {
    display: flex;
  }
  .valid {
    display: flex;
    justify-content: space-between;
    cursor: pointer;
  }
  .valid-input {
    width: 200px;
  }
  .valid-img {
    margin-top: 1px;
    width: 80px;
    height: 38px;
    background: rgb(240, 240, 240);
  }
  .valid-img img {
    width: 80px;
    height: 38px;
  }
</style>