/*
 Navicat MySQL Data Transfer

 Source Server         : 携程
 Source Server Type    : MySQL
 Source Server Version : 80013
 Source Host           : localhost:3306
 Source Schema         : xiecheng

 Target Server Type    : MySQL
 Target Server Version : 80013
 File Encoding         : 65001

 Date: 15/01/2019 16:17:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for hotel
-- ----------------------------
DROP TABLE IF EXISTS `hotel`;
CREATE TABLE `hotel`  (
  `id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `hotel_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dep_date` date NOT NULL,
  `hotel_id` int(11) NOT NULL,
  `start_time` date NOT NULL,
  `room_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `bed_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `breakfast_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` varchar(3000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `room_last` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `pay_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for hotel_id
-- ----------------------------
DROP TABLE IF EXISTS `hotel_id`;
CREATE TABLE `hotel_id`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hotel_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 57 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of hotel_id
-- ----------------------------
INSERT INTO `hotel_id` VALUES (1, 4399431);
INSERT INTO `hotel_id` VALUES (2, 433176);
INSERT INTO `hotel_id` VALUES (3, 1413498);
INSERT INTO `hotel_id` VALUES (4, 661081);
INSERT INTO `hotel_id` VALUES (5, 378777);
INSERT INTO `hotel_id` VALUES (6, 473770);
INSERT INTO `hotel_id` VALUES (7, 433981);
INSERT INTO `hotel_id` VALUES (8, 6278770);
INSERT INTO `hotel_id` VALUES (9, 6657909);
INSERT INTO `hotel_id` VALUES (10, 23852115);
INSERT INTO `hotel_id` VALUES (11, 1064521);
INSERT INTO `hotel_id` VALUES (12, 6338488);
INSERT INTO `hotel_id` VALUES (13, 6874402);
INSERT INTO `hotel_id` VALUES (14, 12517610);
INSERT INTO `hotel_id` VALUES (15, 14074638);
INSERT INTO `hotel_id` VALUES (17, 10355380);
INSERT INTO `hotel_id` VALUES (18, 26102283);
INSERT INTO `hotel_id` VALUES (19, 6758295);
INSERT INTO `hotel_id` VALUES (20, 17284331);
INSERT INTO `hotel_id` VALUES (21, 387009);
INSERT INTO `hotel_id` VALUES (22, 1073814);
INSERT INTO `hotel_id` VALUES (23, 436526);
INSERT INTO `hotel_id` VALUES (24, 19751230);
INSERT INTO `hotel_id` VALUES (25, 345052);
INSERT INTO `hotel_id` VALUES (26, 3893971);
INSERT INTO `hotel_id` VALUES (27, 662503);
INSERT INTO `hotel_id` VALUES (28, 23713263);
INSERT INTO `hotel_id` VALUES (29, 17141864);
INSERT INTO `hotel_id` VALUES (30, 10252911);
INSERT INTO `hotel_id` VALUES (31, 439892);
INSERT INTO `hotel_id` VALUES (32, 437892);
INSERT INTO `hotel_id` VALUES (33, 1480696);
INSERT INTO `hotel_id` VALUES (34, 19613764);
INSERT INTO `hotel_id` VALUES (35, 453317);
INSERT INTO `hotel_id` VALUES (36, 6082325);
INSERT INTO `hotel_id` VALUES (37, 441618);
INSERT INTO `hotel_id` VALUES (38, 6275850);
INSERT INTO `hotel_id` VALUES (39, 3792196);
INSERT INTO `hotel_id` VALUES (40, 5726716);
INSERT INTO `hotel_id` VALUES (41, 8633301);
INSERT INTO `hotel_id` VALUES (42, 6542110);
INSERT INTO `hotel_id` VALUES (43, 1256432);
INSERT INTO `hotel_id` VALUES (44, 1487351);
INSERT INTO `hotel_id` VALUES (45, 3891468);
INSERT INTO `hotel_id` VALUES (46, 1727111);
INSERT INTO `hotel_id` VALUES (47, 16946069);
INSERT INTO `hotel_id` VALUES (48, 3891468);
INSERT INTO `hotel_id` VALUES (49, 446917);
INSERT INTO `hotel_id` VALUES (50, 6399146);
INSERT INTO `hotel_id` VALUES (51, 690633);
INSERT INTO `hotel_id` VALUES (52, 1613365);
INSERT INTO `hotel_id` VALUES (53, 1809284);
INSERT INTO `hotel_id` VALUES (54, 9442151);
INSERT INTO `hotel_id` VALUES (55, 2987364);
INSERT INTO `hotel_id` VALUES (56, 5089316);

SET FOREIGN_KEY_CHECKS = 1;
