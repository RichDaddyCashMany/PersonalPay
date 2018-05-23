# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 123.206.186.27 (MySQL 5.7.20-log)
# Database: personal_pay
# Generation Time: 2018-05-23 07:23:44 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table merchant
# ------------------------------------------------------------

DROP TABLE IF EXISTS `merchant`;

CREATE TABLE `merchant` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `merchant_no` int(11) DEFAULT NULL COMMENT '商户号',
  `username` varchar(16) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `confirm_password` varchar(32) DEFAULT NULL COMMENT '二级密码',
  `phone` int(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `avatar` varchar(200) DEFAULT NULL,
  `parent_no` int(11) DEFAULT NULL COMMENT '上级id',
  `online_from` varchar(14) DEFAULT NULL COMMENT '上线时间开始',
  `online_to` varchar(14) DEFAULT NULL COMMENT '上线时间结束',
  `is_frozen` tinyint(1) DEFAULT NULL,
  `create_at` varchar(14) DEFAULT NULL COMMENT '是否冻结',
  `create_ip` varchar(15) DEFAULT NULL COMMENT '注册ip',
  `login_at` varchar(14) DEFAULT NULL,
  `login_ip` varchar(15) DEFAULT NULL,
  `token` varchar(32) DEFAULT NULL,
  `alipay_name` varchar(20) DEFAULT NULL COMMENT '支付宝姓名',
  `alipay_account` varchar(100) DEFAULT NULL COMMENT '支付宝账号',
  `wechat_name` varchar(20) DEFAULT NULL COMMENT '微信姓名',
  `wechat_account` varchar(100) DEFAULT NULL COMMENT '微信账号',
  PRIMARY KEY (`id`),
  UNIQUE KEY `merchant_no` (`merchant_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商户';



# Dump of table order
# ------------------------------------------------------------

DROP TABLE IF EXISTS `order`;

CREATE TABLE `order` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `merchant_id` int(11) unsigned DEFAULT NULL,
  `product_id` int(11) unsigned DEFAULT NULL,
  `order_no` varchar(32) DEFAULT NULL COMMENT '订单号',
  `platform_order_no` varchar(40) DEFAULT NULL COMMENT '支付平台订单号',
  `platform` int(11) DEFAULT NULL COMMENT '0支付宝 1微信',
  `create_at` varchar(14) DEFAULT NULL,
  `confirm_at` varchar(14) DEFAULT NULL,
  `cost` bigint(11) DEFAULT NULL COMMENT '金额',
  `from_account` varchar(20) DEFAULT NULL COMMENT '来源用户账号',
  `from_nickname` varchar(20) DEFAULT NULL COMMENT '来源用户昵称',
  `from_email` varchar(100) DEFAULT NULL COMMENT '来源邮箱',
  `message` varchar(200) DEFAULT NULL COMMENT '留言',
  `confirm_secret_key` varchar(32) DEFAULT NULL COMMENT '确认密钥',
  PRIMARY KEY (`id`),
  KEY `order_merchant_id` (`merchant_id`),
  KEY `order_product_id` (`product_id`),
  CONSTRAINT `order_merchant_id` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `order_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table product
# ------------------------------------------------------------

DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `merchant_id` int(11) unsigned DEFAULT NULL COMMENT '商户',
  `record_id` varchar(32) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `desc` varchar(100) DEFAULT NULL COMMENT '描述',
  `price` bigint(20) DEFAULT NULL COMMENT '价格',
  `is_on_sell` tinyint(1) DEFAULT NULL COMMENT '0下架 1上架',
  `create_at` varchar(15) DEFAULT NULL,
  `modify_at` varchar(15) DEFAULT NULL COMMENT '修改时间',
  `alipay_qrcode` varchar(200) DEFAULT NULL COMMENT '支付宝收款码',
  `wechat_qrcode` varchar(200) DEFAULT NULL COMMENT '微信收款码',
  PRIMARY KEY (`id`),
  KEY `product_merchant_id` (`merchant_id`),
  CONSTRAINT `product_merchant_id` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table product_stock
# ------------------------------------------------------------

DROP TABLE IF EXISTS `product_stock`;

CREATE TABLE `product_stock` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(11) unsigned DEFAULT NULL,
  `record_id` varchar(32) DEFAULT NULL,
  `content` text,
  `create_at` varchar(14) DEFAULT NULL,
  `sold_at` varchar(14) DEFAULT NULL,
  `order_id` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `stock_product_id` (`product_id`),
  KEY `stock_order_id` (`order_id`),
  CONSTRAINT `stock_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `stock_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
