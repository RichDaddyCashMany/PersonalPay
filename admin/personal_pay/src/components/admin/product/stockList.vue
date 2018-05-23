<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>库存列表</el-breadcrumb-item>
    </el-breadcrumb>

    <div class="top-pannel">
      <el-input placeholder="请输入搜索内容" v-model="searchWords" class="input-with-select">
        <el-select v-model="searchType" slot="prepend" placeholder="请选择">
          <el-option label="商品内容" value="content"></el-option>
        </el-select>
        <el-button slot="append" icon="el-icon-search" @click="onSearch"></el-button>
      </el-input>

      <el-button size="small" type="primary" @click='addStock'>新增库存</el-button>
    </div>
    
    <el-table :data="tableData">
      </el-table-column>
      <el-table-column prop="product_name" label="商品名称" width="160">
      </el-table-column>
      </el-table-column>
      <el-table-column prop="create_at" label="创建时间" width="170">
      </el-table-column>
      <el-table-column prop="sold_at" label="售出时间" width="170">
        <div slot-scope="scope">
          <span class="link" @click="onQueryOrderNO(scope.$index, scope.row)">{{ scope.row.sold_at }}</span>
        </div>
      </el-table-column>
      <el-table-column prop="content" label="商品内容">
        <div slot-scope="scope">
          <span class="content">{{ scope.row.content }}</span>
        </div>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <div slot-scope="scope">
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
        tableData: null,
        pages: 0,
        productId: null,
        searchType: 'content',
        searchWords: ''
      }
    },
    methods: {
      onCurrentChange (page) {
        this.request(page)
      },
      request (page) {
        const size = 10
        api.stockList({
          page: page,
          size: size,
          searchType: this.searchType,
          searchWords: this.searchWords,
          productId: this.productId
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
      addStock () {
        this.$router.push({
          name: 'addStock'
        })
      },
      onDelete (index, row) {
        this.$confirm('是否确定删除？', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'default'
        }).then(() => {
          let data = this.tableData[index]
          api.deleteStock({
            stockId: data.stockId
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
      },
      onQueryOrderNO (index, row) {
        let data = this.tableData[index]
        api.stockOrderNo({
          stockId: data.stockId
        }, (res) => {
          if (res.status === 200) {
            const data = res.data
            this.$router.push({
              name: 'orderList',
              query: {
                order_no: data.data.order_no
              }
            })
          } else {
            this.$message('请求超时')
          }
        })
      }
    },
    created: function () {
      this.productId = this.$route.query.productId
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
    -webkit-line-clamp: 3;
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