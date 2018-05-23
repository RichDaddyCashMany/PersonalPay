<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>订单列表</el-breadcrumb-item>
    </el-breadcrumb>

    <div class="top-pannel">
      <el-input placeholder="请输入搜索内容" v-model="searchWords" class="input-with-select">
        <el-select v-model="searchType" slot="prepend" placeholder="请选择">
          <el-option label="订单号" value="order_no"></el-option>
          <el-option label="支付账号" value="from_account"></el-option>
          <el-option label="收货邮箱" value="from_email"></el-option>
        </el-select>
        <el-button slot="append" icon="el-icon-search" @click="onSearch"></el-button>
      </el-input>
    </div>
    
    <el-table :data="tableData">
      <el-table-column prop="order_no" label="订单号" width="300">
      </el-table-column>
      <el-table-column prop="product_name" label="商品名称" width="160">
        <div slot-scope="scope">
          <span class="link" @click="onStock(scope.$index, scope.row)">{{ scope.row.product_name }}</span>
        </div>
      </el-table-column>
      <el-table-column prop="platform" label="支付方式" width="100">
        <div slot-scope="scope">
          <span>{{ scope.row.platform == '0' ? '支付宝' : '微信' }}</span>
        </div>
      </el-table-column>
      <el-table-column prop="create_at" label="创建时间" width="170">
      </el-table-column>
      <el-table-column prop="confirm_at" label="确认时间" width="170">
      </el-table-column>
      <el-table-column prop="cost" label="金额">
        <div slot-scope="scope">
          <span>{{ scope.row.cost / 100 }}元</span>
        </div>
      </el-table-column>
      <el-table-column prop="from_account" label="支付账号" width="180">
      </el-table-column>
      <el-table-column prop="from_email" label="收货邮箱" width="180">
      </el-table-column>
      <el-table-column prop="from_nickname" label="支付姓名">
      </el-table-column>
      <el-table-column prop="message" label="留言">
        <div slot-scope="scope">
          <span class="content">{{ scope.row.message }}</span>
        </div>
      </el-table-column>
      <el-table-column label="操作" width="100" fixed="right">
        <div slot-scope="scope">
          <el-button
          size="mini" 
          type="primary" 
          @click="onConfirm(scope.$index, scope.row)"
          :disabled="scope.row.confirm_at ? true : false">{{scope.row.confirm_at ? '订单完成' : '确认收款'}}
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
        tableData: null,
        pages: 0,
        searchType: 'order_no',
        searchWords: ''
      }
    },
    methods: {
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
      onCurrentChange (page) {
        this.request(page)
      },
      request (page) {
        const size = 10
        api.orderList({
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
      onSearch () {
        this.request(1)
      },
      onConfirm (index, row) {
        this.$confirm('确认收货后，会立即向买家的邮箱发货哦！', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'default'
        }).then(() => {
          let data = this.tableData[index]
          api.orderConfirm({
            order_no: data.order_no
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
      }
    },
    created: function () {
      this.searchWords = this.$route.query.order_no ? this.$route.query.order_no : ''
      this.request(1)
    }
  }
</script>

<style scoped>
  @import '../../../css/common.css';
  
  .top-pannel {
    margin-bottom: 30px;
    width: 600px;
  }
  img.head {
    width: 40px;
    height: 40px;
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