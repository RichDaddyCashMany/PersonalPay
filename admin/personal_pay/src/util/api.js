import axios from 'axios'
import router from '../router'

/**
 * 因为在index.js中的proxyTable配置了代理没效果，所幸在这里配置
 */
let MAIN_URL = ''
if (process.env.NODE_ENV === 'development') {
  MAIN_URL = 'http://127.0.0.1:5000'
} else {
  MAIN_URL = 'http://123.206.186.27:82'
}

const request = (url, data, callback) => {
  axios.post(MAIN_URL + '/' + url, data)
  .then((response) => {
    if (response &&
      response.status === 200 &&
      response.data.code === 1001) {
      // need login
      router.push({
        name: 'login'
      })
    }
    callback(response)
  })
}

/**
 * reg
 */
const reg = (params, callback) => {
  var data = new URLSearchParams()
  data.append('username', params.username)
  data.append('password', params.password)
  data.append('password2', params.password2)
  data.append('validId', params.validId)
  data.append('validValue', params.validValue)

  request('merchant/reg', data, (response) => {
    callback(response)
  })
}

/**
 * login
 */
const login = (params, callback) => {
  var data = new URLSearchParams()
  data.append('username', params.username)
  data.append('password', params.password)

  request('merchant/login', data, (response) => {
    if (response &&
      response.status === 200 &&
      response.data.code === 0) {
      localStorage.token = response.data.data.token // save token to localStorage
    }
    callback(response)
  })
}

const merchantInfo = (params, callback) => {
  // console.log(params)
  var data = new URLSearchParams()
  data.append('token', localStorage.token)

  request('merchant/info', data, (response) => {
    callback(response)
  })
}

const merchantInfoSave = (params, callback) => {
  // console.log(params)
  var data = new URLSearchParams()
  data.append('token', localStorage.token)
  data.append('email', params.email ? params.email : '')
  data.append('online_from', params.online_from ? params.online_from : '')
  data.append('online_to', params.online_to ? params.online_to : '')
  data.append('alipay_name', params.alipay_name ? params.alipay_name : '')
  data.append('alipay_account', params.alipay_account ? params.alipay_account : '')
  data.append('wechat_name', params.wechat_name ? params.wechat_name : '')
  data.append('wechat_account', params.wechat_account ? params.wechat_account : '')

  request('merchant/info/save', data, (response) => {
    callback(response)
  })
}

const addProduct = (params, callback) => {
  // console.log(params)
  var data = new URLSearchParams()
  data.append('token', localStorage.token)
  data.append('name', params.name)
  data.append('desc', params.desc)
  data.append('price', params.price * 100)
  data.append('alipay_qrcode', params.alipay_qrcode)
  data.append('wechat_qrcode', params.wechat_qrcode)
  data.append('productId', params.productId)
  data.append('is_on_sell', params.is_on_sell)

  request('product/add', data, (response) => {
    callback(response)
  })
}

const productList = (params, callback) => {
  // console.log(params)
  var data = new URLSearchParams()
  data.append('token', localStorage.token)
  data.append('page', params.page)
  data.append('size', params.size)
  data.append('searchType', params.searchType)
  data.append('searchWords', params.searchWords)

  request('product/list', data, (response) => {
    callback(response)
  })
}

const deleteProduct = (params, callback) => {
  // console.log(params)
  var data = new URLSearchParams()
  data.append('token', localStorage.token)
  data.append('productId', params.productId)

  request('product/delete', data, (response) => {
    callback(response)
  })
}

const addStock = (params, callback) => {
  // console.log(params)
  var data = new URLSearchParams()
  data.append('token', localStorage.token)
  data.append('productId', params.productId)
  data.append('content', params.content)

  request('product/stock/add', data, (response) => {
    callback(response)
  })
}

const stockList = (params, callback) => {
  // console.log(params)
  var data = new URLSearchParams()
  data.append('token', localStorage.token)
  data.append('productId', params.productId)
  data.append('page', params.page)
  data.append('size', params.size)
  data.append('searchType', params.searchType)
  data.append('searchWords', params.searchWords)

  request('product/stock/list', data, (response) => {
    callback(response)
  })
}

const deleteStock = (params, callback) => {
  // console.log(params)
  var data = new URLSearchParams()
  data.append('token', localStorage.token)
  data.append('stockId', params.stockId)

  request('product/stock/delete', data, (response) => {
    callback(response)
  })
}

const stockOrderNo = (params, callback) => {
  // console.log(params)
  var data = new URLSearchParams()
  data.append('token', localStorage.token)
  data.append('stockId', params.stockId)

  request('product/stock/orderno', data, (response) => {
    callback(response)
  })
}

const orderList = (params, callback) => {
  // console.log(params)
  var data = new URLSearchParams()
  data.append('token', localStorage.token)
  data.append('page', params.page)
  data.append('size', params.size)
  data.append('searchType', params.searchType)
  data.append('searchWords', params.searchWords)

  request('order/list', data, (response) => {
    callback(response)
  })
}

const orderConfirm = (params, callback) => {
  // console.log(params)
  var data = new URLSearchParams()
  data.append('token', localStorage.token)
  data.append('order_no', params.order_no)

  request('order/confirm', data, (response) => {
    callback(response)
  })
}

const qcloudToken = (params, callback) => {
  var data = new URLSearchParams()
  data.append('token', localStorage.token)

  request('common/QCloud/sign', data, (response) => {
    if (response &&
      response.status === 200 &&
      response.data.code === 0) {
      callback(response)
    }
    callback(response)
  })
}

const getValidImage = (params, callback) => {
  // console.log(params)
  request('common/validImage/create', params, (response) => {
    callback(response)
  })
}

const api = {
  reg: reg,
  login: login,
  qcloudToken: qcloudToken,
  getValidImage: getValidImage,
  addProduct: addProduct,
  productList: productList,
  deleteProduct: deleteProduct,
  addStock: addStock,
  stockList: stockList,
  deleteStock: deleteStock,
  orderList: orderList,
  orderConfirm: orderConfirm,
  stockOrderNo: stockOrderNo,
  merchantInfo: merchantInfo,
  merchantInfoSave: merchantInfoSave
}

export default api
