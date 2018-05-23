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
        <el-form-item label="确认密码" prop="password2">
          <el-input v-model="form.password2" auto-complete="off" type="password"></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="validValue">
          <div class="valid">
            <el-input class="valid-input" v-model="form.validValue" auto-complete="off"></el-input>
            <div class="valid-img" @click="getValidImage">
              <img :src="validImg">
            </div>
          </div>
        </el-form-item>
        <el-form-item class="button-container">
          <el-button type="primary" :loading="regButtonLoading" @click="submitForm">注册账号</el-button>
          <el-button type="default" @click="onGotoLogin">返回登录</el-button>
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
        regButtonLoading: false,
        form: {
          username: '',
          password: '',
          password2: '',
          validValue: '',
          validId: ''
        },
        validImg: '',
        rules: {
          username: [
            {
              validator: (rule, value, callback) => {
                if (value === '') {
                  callback(new Error('请输入账号'))
                } else if (value.length < 6) {
                  callback(new Error('账号长度必须大于6位'))
                }
                callback()
              },
              trigger: 'blur',
              required: true
            }
          ],
          password: [
            {
              validator: (rule, value, callback) => {
                if (value === '') {
                  callback(new Error('请输入密码'))
                } else if (value.length < 6) {
                  callback(new Error('密码长度必须大于6位'))
                }
                callback()
              },
              trigger: 'blur',
              required: true
            }
          ],
          password2: [
            {
              validator: (rule, value, callback) => {
                if (value === '') {
                  callback(new Error('请输入密码'))
                } else if (value.length < 6) {
                  callback(new Error('密码长度必须大于6位'))
                } else if (value !== this.form.password) {
                  callback(new Error('两次密码不一致'))
                }
                callback()
              },
              trigger: 'blur',
              required: true
            }
          ],
          validValue: [
            { required: true, message: '请输入验证码', trigger: 'blur' }
          ]
        }
      }
    },
    methods: {
      getValidImage () {
        api.getValidImage({
          type: '0'
        }, (res) => {
          if (res.status === 200) {
            const data = res.data
            if (data.code === 0) {
              this.form.validId = data.data.sendId
              this.validImg = data.data.img
            } else {
              this.$message(data.message)
            }
          } else {
            this.$message('验证码请求超时')
          }
        })
      },
      submitForm () {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            this.requestReg()
          } else {
            return false
          }
        })
      },
      onGotoLogin () {
        this.$router.push({name: 'login'})
      },
      requestReg () {
        this.regButtonLoading = true

        api.reg({
          'username': this.form.username,
          'password': this.form.password,
          'password2': this.form.password2,
          'validValue': this.form.validValue,
          'validId': this.form.validId
        }, (res) => {
          this.regButtonLoading = false

          if (res.status === 200) {
            const data = res.data
            if (data.code === 0) {
              this.$message('注册成功')
              this.onGotoLogin()
            } else {
              this.getValidImage()
              this.$message(data.message)
            }
          } else {
            this.$message('请求超时')
          }
        })
      }
    },
    created: function () {
      this.getValidImage()
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