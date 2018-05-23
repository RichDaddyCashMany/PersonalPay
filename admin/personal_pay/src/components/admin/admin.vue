<template>
  <el-container>

    <el-container>
      <el-header>
        <div class="logo-wrap" @click="onGoHome">
          <img class="logo" src="../../images/logo.png">
        </div>
        <el-dropdown>
          <span class="el-dropdown-link">
            欢迎您！{{username}}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item @click.native="onExitAccount">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-header>
      
      <el-main>
        <!-- 内容区域 -->
        <router-view></router-view>
      </el-main>

    </el-container>

    <el-aside width="200px">
      <el-menu :default-openeds="['1', '2', '3']" :default-active="menuIndex">
        <el-submenu index="1">
          <template slot="title">商户管理</template>
          <el-menu-item-group>
            <el-menu-item index="1-0" @click="onMenuChange('merchantDetail')">商户信息</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">商品管理</template>
          <el-menu-item-group>
            <el-menu-item index="2-0" @click="onMenuChange('productList')">商品列表</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group>
            <el-menu-item index="2-1" @click="onMenuChange('stockList')">库存列表</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="3">
          <template slot="title">订单管理</template>
          <el-menu-item-group>
            <el-menu-item index="3-0" @click="onMenuChange('orderList')">订单列表</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
      </el-menu>
    </el-aside>
    
  </el-container>
</template>

<script>
  import common from '../../util/common.js'
  export default {
    data () {
      return {
        username: localStorage.username
      }
    },
    methods: {
      onMenuChange (page, fromHook) { // 菜单状态缓存
        const indexs = [
          {
            'index': '1-0',
            'pages': ['merchantDetail']
          },
          {
            'index': '2-0',
            'pages': ['productList', 'addProduct']
          },
          {
            'index': '2-1',
            'pages': ['stockList', 'addStock']
          },
          {
            'index': '3-0',
            'pages': ['orderList']
          }
        ]

        for (var i = 0; i < indexs.length; i++) {
          const dic = indexs[i]
          if (common.isInArray(dic['pages'], page)) {
            this.$store.commit('changeMenuIndex', dic['index'])
            break
          }
        }

        if (!fromHook) {
          this.$router.push({
            name: page
          })
        }
      },
      onExitAccount () {
        this.$confirm('是否退出当前账号？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'default'
        }).then(() => {
          localStorage.removeItem('token')
          this.$router.push({
            name: 'login'
          })
        }).catch(() => {
        })
      },
      onGoHome () {
        window.location = 'http://www.51shuaba.xyz'
      }
    },
    computed: {
      menuIndex: function () {
        return this.$store.state.menuIndex
      }
    },
    created: function () {
      if (!localStorage.token) {
        this.$router.push({
          name: 'login'
        })
      }
      // 全局路由钩子，监听浏览器前进后退
      this.$router.beforeEach((to, from, next) => {
        next()
        this.onMenuChange(to.name, true)
      })
      this.$router.afterEach((to, from) => {
        this.onMenuChange(to.name, true)
      })
    },
    beforeRouteEnter: (to, from, next) => { // 监听刷新页面
      next(vm => {
        vm.onMenuChange(to.name, true)
      })
    }
  }
</script>

<style scoped>
  .logo-wrap {
    height: 60px;
    display: flex;
    align-items: center;
    cursor: pointer;
  }
  .logo {
    height: 20px;
  }
  .el-dropdown-link {
    cursor: pointer;
    font-size: 13px;
    color: #333;
    font-weight: 400;
  }
  .el-icon-arrow-down {
    font-size: 14px;
  }
  .el-header {
    font-size: 12px;
    position: fixed;
    left: 0;
    right: 0;
    top: 0;
    line-height: 60px;
    z-index: 999;
    display: flex;
    justify-content: space-between;
    border: 1px solid transparent;
    background-color: white;
    border-width: 0px 0 1px;
    border-color: #f0f0f0;
  }
  .title {
    font-size: 20px;
  }
  .el-aside {
    color: #333;
    position: fixed;
    left: 0;
    top: 60px;
    bottom: 0;
    background-color: rgb(248, 248, 248);
  }
  .el-menu {
    border-right: 1px solid rgb(248,248,248);
  }
  .el-main {
    position: absolute;
    left: 200px;
    top: 60px;
    right: 0;
    bottom: 0;
  }
  .el-table {
    margin-bottom: 20px;
  }
  .el-pagination {
    margin-bottom: 20px;
  }
  .el-menu-item {
    height: 40px;
    line-height: 40px;
  }
</style>