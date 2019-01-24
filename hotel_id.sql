/*
 Navicat Premium Data Transfer

 Source Server         : 携程
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : xiecheng

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 23/01/2019 20:18:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for hotel_id
-- ----------------------------
DROP TABLE IF EXISTS `hotel_id`;
CREATE TABLE `hotel_id`  (
  `hotel_id` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`, `hotel_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of hotel_id
-- ----------------------------
INSERT INTO `hotel_id` VALUES (369710, 1);

SET FOREIGN_KEY_CHECKS = 1;
