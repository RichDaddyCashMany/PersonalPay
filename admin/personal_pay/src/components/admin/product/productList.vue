<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品列表</el-breadcrumb-item>
    </el-breadcrumb>
    
    <div class="top-pannel">
      <el-input placeholder="请输入搜索内容" v-model="searchWords" class="input-with-select">
        <el-select v-model="searchType" slot="prepend" placeholder="请选择">
          <el-option label="商品名称" value="product_name"></el-option>
        </el-select>
        <el-button slot="append" icon="el-icon-search" @click="onSearch"></el-button>
      </el-input>

      <el-button size="small" type="primary" @click='addProduct'>新增商品</el-button>
    </div>

    <el-table :data="tableData">
      <el-table-column prop="name" label="商品名称">
        <div slot-scope="scope">
          <span class="link" @click="onStock(scope.$index, scope.row)">{{ scope.row.name }}</span>
        </div>
      </el-table-column>
      <el-table-column prop="price" label="商品价格" width="140">
        <div slot-scope="scope">
          <span>{{ scope.row.price / 100 }}元</span>
        </div>
      </el-table-column>
      <el-table-column prop="create_at" label="创建时间" width="170">
      </el-table-column>
      <el-table-column prop="is_on_sell" label="是否上架中" width="170">
        <div slot-scope="scope">
          <span>{{ scope.row.is_on_sell === 0 ? '否' : '是' }}</span>
        </div>
      </el-table-column>
      <el-table-column prop="desc" label="描述">
        <div slot-scope="scope">
          <span class="content">{{ scope.row.desc }}</span>
        </div>
      </el-table-column>
      <el-table-column label="操作" width="240">
        <div slot-scope="scope">
          <el-button
          size="mini" 
          @click="onEdit(scope.$index, scope.row)">编辑
          </el-button>
          <el-button
            size="mini"
            type="danger" 
            @click="onDelete(scope.$index, scope.row)"
            :disabled="scope.row.enable === '0'">删除
          </el-button>
        </div>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        layout="prev, pager, next"
        :total="pages"
        @current-change="onCurrentChange">
      </el-pagination>
      <p class="count">共{{pages}}条记录</p>
    </div>
  </div>
</template>

<script>
  import api from '../../../util/api.js'

  export default {
    data () {
      return {
        noticeType: '0',
        tableData: null,
        pages: 0,
        searchType: 'product_name',
        searchWords: ''
      }
    },
    methods: {
      onCurrentChange (page) {
        this.request(page)
      },
      request (page) {
        const size = 10
        api.productList({
          page: page,
          size: size,
          searchType: this.searchType,
          searchWords: this.searchWords
        }, (res) => {
          if (res.status === 200) {
            const data = res.data
            if (data.code === 0) {
              this.tableData = data.data.list
              this.pages = data.data.totalCount
            } else {
              this.$message(data.message)
            }
          } else {
            this.$message('请求超时')
          }
        })
      },
      addProduct () {
        this.$router.push({
          name: 'addProduct'
        })
      },
      onEdit (index, row) {
        let data = this.tableData[index]
        console.log(data)
        let form = {
          productId: data.productId,
          name: data.name,
          price: data.price / 100,
          desc: data.desc,
          alipay_qrcode: data.alipay_qrcode,
          wechat_qrcode: data.wechat_qrcode,
          is_on_sell: data.is_on_sell + ''
        }
        // 跳转
        this.$router.push({
          name: 'addProduct',
          query: form
        })
      },
      onStock (index, row) {
        let data = this.tableData[index]
        // 跳转
        this.$router.push({
          name: 'stockList',
          query: {
            productId: data.productId
          }
        })
      },
      onDelete (index, row) {
        this.$confirm('删除商品会连库存一起删除，是否确定删除？', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'default'
        }).then(() => {
          let data = this.tableData[index]
          api.deleteProduct({
            productId: data.productId
          }, (res) => {
            if (res.status === 200) {
              const data = res.data
              this.$message(data.message)
              this.request(1)
            } else {
              this.$message('请求超时')
            }
          })
        }).catch(() => {
        })
      },
      onSearch () {
        this.request(1)
      }
    },
    created: function () {
      this.request(1)
    }
  }
</script>

<style scoped>
  @import '../../../css/common.css';
  
  .top-pannel {
    display: flex;
    margin-bottom: 20px;
    justify-content: space-between;
  }
  .input-with-select {
    width: 600px;
  }
  span.content {
    text-overflow: -o-ellipsis-lastline;  
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
  .link {
    text-decoration: underline;
    cursor: pointer;
    color: black;
  }
  .link:hover {
    color: #409EFF;
  }
</style>