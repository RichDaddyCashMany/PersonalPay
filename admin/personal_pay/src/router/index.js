import Vue from 'vue'
import Router from 'vue-router'
import notFound from '@/components/common/404'
import admin from '@/components/admin/admin'
import reg from '@/components/common/reg'
import login from '@/components/common/login'
import merchantDetail from '@/components/admin/merchant/detail'
import productList from '@/components/admin/product/productList'
import addProduct from '@/components/admin/product/addProduct'
import addStock from '@/components/admin/product/addStock'
import stockList from '@/components/admin/product/stockList'
import orderList from '@/components/admin/order/orderList'

Vue.use(Router)

const dic = {
  routes: [
    {
      path: '/admin',
      title: '管理台',
      name: 'admin',
      component: admin,
      redirect: { name: 'merchantDetail' },
      children: [
        {
          path: 'productList',
          title: '商品列表',
          name: 'productList',
          component: productList
        },
        {
          path: 'merchantDetail',
          name: 'merchantDetail',
          component: merchantDetail
        },
        {
          path: 'addProduct',
          name: 'addProduct',
          component: addProduct
        },
        {
          path: 'addStock',
          name: 'addStock',
          component: addStock
        },
        {
          path: 'stockList',
          name: 'stockList',
          component: stockList
        },
        {
          path: 'orderList',
          name: 'orderList',
          component: orderList
        }
      ]
    },
    {
      path: '/login',
      title: '登录',
      name: 'login',
      component: login
    },
    {
      path: '/reg',
      title: '注册',
      name: 'reg',
      component: reg
    },
    {
      path: '/wrongway',
      component: notFound,
      name: 'notFound',
      hidden: true
    },
    {
      path: '*',
      hidden: true,
      redirect: { name: 'notFound' }
    },
    {
      path: '/',
      hidden: true,
      redirect: { name: 'merchantDetail' }
    }
  ],
  mode: 'history'
}

export default new Router(dic)
