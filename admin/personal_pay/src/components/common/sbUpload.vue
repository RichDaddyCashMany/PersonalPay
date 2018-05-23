<template>
  <div>
    <a href="javascript:;" class="upload">
      <span v-if="!value">+</span>
      <img class="upload-img" :src="value">
      <input type="file" class="upload-file" @change="fileChange">
      <input type="text" ref="input" :value="value" @input="$emit('input', $event.target.value)" hidden>
    </a>
    <el-button style="margin-top: 10px;" size="mini" type="primary" @click="preview" v-if="showButton">查看大图</el-button>
  </div>
</template>

<script>
  import qcloud from '../../util/qcloud.js'

  export default {
    data () {
      return {
        showButton: false
      }
    },
    props: ['value', 'showButton'],
    methods: {
      fileChange (e) {
        console.log('begin upload')
        qcloud.upload(e, (url) => {
          this.$message('上传成功')
          this.$emit('input', url)
        }, () => {
          this.$message('上传失败')
        })
      },
      preview () {
        if (!this.value) {
          this.$message('请先上传图片')
        } else {
          this.$alert('<img src="' + this.value + '">', '查看大图', {
            dangerouslyUseHTMLString: true
          })
        }
      }
    },
    created: function () {
    }
  }
</script>

<style scoped>
  .avatar {
    display: block;
  }
  span {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }
  a.upload {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    text-decoration: none;
    text-indent: 0;
    line-height: 178px;
    text-align: center;
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  a.upload:hover {
    border: 1px dashed #409EFF;
  }
  a.upload .upload-img {
    max-width: 178px;
    max-height: 178px;
  }
  a.upload .upload-img[src=""]{
    opacity: 0;
  }
  a.upload .upload-file {
    position: absolute;
    right: 0;
    top: 0;
    opacity: 0;
    width: 178px;
    height: 178px;
  }
  .el-message-box__message {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .el-message-box__message p img {
    height: 600px;
  }
</style>