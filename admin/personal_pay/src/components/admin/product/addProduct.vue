<template>
  <div class="container">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品列表</el-breadcrumb-item>
      <el-breadcrumb-item>{{ pageTitle }}</el-breadcrumb-item>
    </el-breadcrumb>

    <el-form :model="form" :rules="rules" ref="form" label-width="100px" class="form">
      <input type="text" name="productId" :value="form.productId" hidden>
      <el-form-item label="商品名称" prop="name" label-width="140px">
        <el-input v-model="form.name" auto-complete="off" :disabled="form.productId.length > 0"></el-input>
      </el-form-item>
      <el-form-item label="商品价格（元）" prop="price" label-width="140px">
        <el-input v-model="form.price" auto-complete="off" placeholder="最多保留两位小数"></el-input>
      </el-form-item>
      <el-form-item label="商品介绍" label-width="140px">
          <el-input type="textarea" v-model="form.desc" :rows="3"></el-input>
      </el-form-item>
      <el-form-item label="支付宝收款码" prop="alipay_qrcode" label-width="140px">
        <sb-upload v-model="form.alipay_qrcode" :showButton="false"></sb-upload>
        <el-tag type="info" v-if="form.price">请上传金额为 ￥{{form.price}} 的二维码正方形图片</el-tag>
      </el-form-item>
      <el-form-item label="微信收款码" prop="wechat_qrcode" label-width="140px">
        <sb-upload v-model="form.wechat_qrcode" :showButton="false"></sb-upload>
        <el-tag type="info" v-if="form.price">请上传金额为 ￥{{form.price}} 的二维码正方形图片</el-tag>
      </el-form-item>
      <el-form-item label="是否上架" v-if="form.productId" label-width="140px">
        <el-switch v-model="form.is_on_sell" active-value='1' inactive-value='0'></el-switch>
      </el-form-item>
      <el-form-item class="button-container" label-width="140px">
        <el-button type="primary" :loading="buttonLoading" @click="submitForm">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import api from '../../../util/api.js'
  import sbUpload from '../../common/sbUpload.vue'
  import common from '../../../util/common.js'

  export default {
    data () {
      return {
        pageTitle: '',
        buttonLoading: false,
        form: {
          productId: '',
          name: '',
          price: '',
          desc: '',
          alipay_qrcode: '',
          wechat_qrcode: '',
          is_on_sell: ''
        },
        rules: {
          name: [
            {
              validator: (rule, value, callback) => {
                if (value === '') {
                  callback(new Error('请输入标题'))
                } else if (value.length > 10) {
                  callback(new Error('标题长度不能大于20个字符'))
                }
                callback()
              },
              trigger: 'blur',
              required: true
            }
          ],
          price: [
            {
              validator: (rule, value, callback) => {
                if (value === '') {
                  callback(new Error('请输入价格'))
                }
                callback()
              },
              trigger: 'blur',
              required: true
            }
          ],
          alipay_qrcode: [
            {
              validator: (rule, value, callback) => {
                if (value === '') {
                  callback(new Error('请选择图片'))
                }
                callback()
              },
              trigger: 'blur',
              required: true
            }
          ],
          wechat_qrcode: [
            {
              validator: (rule, value, callback) => {
                if (value === '') {
                  callback(new Error('请选择图片'))
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
    components: {
      sbUpload
    },
    methods: {
      submitForm () {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            this.request()
          } else {
            this.$message('还有未完成的必填选项')
            return false
          }
        })
      },
      request () {
        this.buttonLoading = false

        api.addProduct(this.form, (res) => {
          this.buttonLoading = false

          if (res.status === 200) {
            const data = res.data
            if (data.code === 0) {
              this.$message('提交成功')
              this.$router.push({
                name: 'productList'
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
      this.form = common.safeKeyValueAssign(this.form, this.$route.query)
      console.log(this.form)

      if (this.form.productId) {
        this.pageTitle = '编辑商品'
      } else {
        this.pageTitle = '新增商品'
      }
    }
  }
</script>

<style scoped>
  @import '../../../css/common.css';

  div.container {
    width: 600px;
  }
</style>