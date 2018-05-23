<template>
  <div class="container">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>库存列表</el-breadcrumb-item>
      <el-breadcrumb-item>新增库存</el-breadcrumb-item>
    </el-breadcrumb>

    <el-form :model="form" :rules="rules" ref="form" label-width="100px" class="form">
      <input type="text" name="productId" :value="form.productId" hidden>
      <el-form-item label="商品名称" prop="productId" label-width="140px">
         <el-select v-model="form.productId" placeholder="请选择">
          <el-option
            v-for="product in products"
            :key="product.productId"
            :label="product.name"
            :value="product.productId">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="商品内容" label-width="140px" prop="content">
          <el-input type="textarea" v-model="form.content" :rows="20"></el-input>
          <el-tag type="info">如有多条商品，请使用 #separator# 分隔（包含#号）</el-tag>
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
        products: [],
        buttonLoading: false,
        form: {
          productId: '',
          content: ''
        },
        rules: {
          productId: [
            {
              validator: (rule, value, callback) => {
                if (value === '') {
                  callback(new Error('请选择商品'))
                }
                callback()
              },
              trigger: 'blur',
              required: true
            }
          ],
          content: [
            {
              validator: (rule, value, callback) => {
                if (value === '') {
                  callback(new Error('商品内容不能为空'))
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

        api.addStock(this.form, (res) => {
          this.buttonLoading = false

          if (res.status === 200) {
            const data = res.data
            if (data.code === 0) {
              this.$message('提交成功')

              let productName = ''
              for (var i = 0; i < this.products.length; i++) {
                const product = this.products[i]
                if (product.productId === this.form.productId) {
                  productName = product.name
                  break
                }
              }

              this.$router.push({
                name: 'stockList',
                query: {
                  productId: this.form.productId,
                  productName: productName
                }
              })
            } else {
              this.$message(data.message)
            }
          } else {
            this.$message('请求超时')
          }
        })
      },
      requestProducts () {
        api.productList({
          page: 1,
          size: 100,
          searchType: '',
          searchWords: ''
        }, (res) => {
          if (res.status === 200) {
            const data = res.data
            if (data.code === 0) {
              this.products = data.data.list
            } else {
              this.$message(data.message)
            }
          } else {
            this.$message('请求商品列表超时')
          }
        })
      }
    },
    created: function () {
      this.requestProducts()
      this.form = common.safeKeyValueAssign(this.form, this.$route.query)

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