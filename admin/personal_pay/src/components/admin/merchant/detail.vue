<template>
  <div class="container">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>商户信息</el-breadcrumb-item>
    </el-breadcrumb>

    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="修改信息" name="first">
        <el-form :model="form" :rules="rules" ref="form" label-width="100px" class="form">
          <el-form-item label="确认收款邮箱" prop="email" label-width="140px">
            <el-input v-model="form.email" auto-complete="off" placeholder=""></el-input>
            <el-tag type="info">建议使用邮箱类手机App，随时随地确认收款</el-tag>
          </el-form-item>
          <el-form-item label="收款支付宝" label-width="140px">
            <el-input v-model="form.alipay_name" auto-complete="off" placeholder="支付宝昵称"></el-input>
          </el-form-item>
          <el-form-item label="收款微信" label-width="140px">
            <el-input v-model="form.wechat_name" auto-complete="off"  placeholder="微信昵称"></el-input>
          </el-form-item>
          <el-form-item label="商户在线时间" label-width="140px">
            <el-time-select
              placeholder="起始时间"
              v-model="form.online_from"
              :picker-options="{
                start: '00:30',
                step: '00:30',
                end: '23:30'
              }">
            </el-time-select>
          </el-form-item>
          <el-form-item label="" label-width="140px">
            <el-time-select
              placeholder="结束时间"
              v-model="form.online_to"
              :picker-options="{
                start: '00:30',
                step: '00:30',
                end: '23:30'
              }">
            </el-time-select>
          </el-form-item>
          <el-form-item class="button-container" label-width="140px">
            <el-button type="primary" :loading="buttonLoading" @click="submitForm">提交</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="收款链接" name="second">
        <div class="showkuan">
          <el-tag>{{mch_url}}</el-tag>
        </div>
      </el-tab-pane>
    </el-tabs>

  </div>
</template>

<script>
  import api from '../../../util/api.js'

  export default {
    data () {
      return {
        activeName: 'first',
        mch_url: '',
        form: {
          email: '',
          alipay_name: '',
          alipay_account: '',
          wechat_name: '',
          wechat_account: '',
          online_from: '',
          online_to: ''
        },
        rules: {
          email: [
            {
              validator: (rule, value, callback) => {
                if (value === '') {
                  callback(new Error('请输入邮箱'))
                }
                callback()
              },
              trigger: 'blur',
              required: true
            }
          ]
        }
      }
    },
    methods: {
      submitForm () {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            this.onSubmit()
          } else {
            this.$message('还有未完成的必填选项')
            return false
          }
        })
      },
      onSubmit () {
        api.merchantInfoSave(this.form, (res) => {
          if (res.status === 200) {
            const data = res.data
            if (data.code === 0) {
              this.$message('提交成功')
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
      api.merchantInfo(null, (res) => {
        if (res.status === 200) {
          const data = res.data
          if (data.code === 0) {
            this.form = data.data
            this.mch_url = data.data.mch_url
          } else {
            this.$message(data.message)
          }
        } else {
          this.$message('请求超时')
        }
      })
    }
  }
</script>

<style scoped>
  @import '../../../css/common.css';
  .form {
    margin-top: 20px;
    width: 500px;
  }
  .showkuan {
    padding-left: 20px;
    margin-top: 20px;
  }
</style>