-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- 主机： 127.0.0.1
-- 生成日期： 2019-04-04 01:25:02
-- 服务器版本： 5.7.24
-- PHP 版本： 7.1.19
use manifoldb;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `manifoldb`
--

-- --------------------------------------------------------

--
-- 表的结构 `ahpjudgement`
--

CREATE TABLE `ahpjudgement` (
  `id` int(11) NOT NULL,
  `indexid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `cid` int(11) DEFAULT NULL,
  `value` float DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `ahpjudgement`
--

INSERT INTO `ahpjudgement` (`id`, `indexid`, `pid`, `cid`, `value`) VALUES
(502, 1, 0, 1, 1),
(503, 1, 0, 2, 0.5),
(504, 1, 0, 3, 0.14),
(505, 2, 0, 1, 2),
(506, 2, 0, 2, 1),
(507, 2, 0, 3, 0.14),
(508, 3, 0, 1, 7),
(509, 3, 0, 2, 7),
(510, 3, 0, 3, 1),
(511, 4, 1, 4, 1),
(512, 4, 1, 5, 0.2),
(513, 4, 1, 6, 0.33),
(514, 4, 1, 7, 0.25),
(515, 5, 1, 4, 5),
(516, 5, 1, 5, 1),
(517, 5, 1, 6, 3),
(518, 5, 1, 7, 1),
(519, 6, 1, 4, 3),
(520, 6, 1, 5, 0.33),
(521, 6, 1, 6, 1),
(522, 6, 1, 7, 0.2),
(523, 7, 1, 4, 4),
(524, 7, 1, 5, 1),
(525, 7, 1, 6, 5),
(526, 7, 1, 7, 1),
(527, 8, 2, 8, 1),
(528, 8, 2, 9, 5),
(529, 8, 2, 10, 0.5),
(530, 8, 2, 11, 7),
(531, 8, 2, 12, 4),
(532, 9, 2, 8, 0.2),
(533, 9, 2, 9, 1),
(534, 9, 2, 10, 0.14),
(535, 9, 2, 11, 2),
(536, 9, 2, 12, 1),
(537, 10, 2, 8, 2),
(538, 10, 2, 9, 7),
(539, 10, 2, 10, 1),
(540, 10, 2, 11, 9),
(541, 10, 2, 12, 7),
(542, 11, 2, 8, 0.14),
(543, 11, 2, 9, 0.5),
(544, 11, 2, 10, 0.11),
(545, 11, 2, 11, 1),
(546, 11, 2, 12, 0.2),
(547, 12, 2, 8, 0.25),
(548, 12, 2, 9, 1),
(549, 12, 2, 10, 0.14),
(550, 12, 2, 11, 5),
(551, 12, 2, 12, 1),
(552, 13, 3, 13, 1),
(553, 13, 3, 14, 4),
(554, 14, 3, 13, 0.25),
(555, 14, 3, 14, 1);

-- --------------------------------------------------------

--
-- 表的结构 `ahp_tree`
--

CREATE TABLE `ahp_tree` (
  `id` int(11) NOT NULL,
  `pid` int(11) NOT NULL DEFAULT '-1',
  `importance` float DEFAULT '0',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `createdby` int(11) DEFAULT '1' COMMENT '创建人'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `ahp_tree`
--

INSERT INTO `ahp_tree` (`id`, `pid`, `importance`, `create_time`, `createdby`) VALUES
(1, 0, 0.084, '2018-05-29 07:15:18', 1),
(2, 0, 0.114, '2018-05-29 07:15:18', 1),
(3, 0, 0.802, '2018-05-29 07:15:18', 1),
(4, 1, 0.006, '2018-05-29 07:15:18', 1),
(5, 1, 0.0315, '2018-05-29 07:15:18', 1),
(6, 1, 0.0089, '2018-05-29 07:15:18', 1),
(7, 1, 0.0375, '2018-05-29 07:15:18', 1),
(8, 2, 0.0343, '2018-05-29 07:15:18', 1),
(9, 2, 0.0087, '2018-05-29 07:15:18', 1),
(10, 2, 0.0546, '2018-05-29 07:15:18', 1),
(11, 2, 0.0042, '2018-05-29 07:15:18', 1),
(12, 2, 0.0122, '2018-05-29 07:15:18', 1),
(13, 3, 0.6416, '2018-05-29 07:15:18', 1),
(14, 3, 0.1604, '2018-05-29 07:15:18', 1);

-- --------------------------------------------------------

--
-- 表的结构 `assessment`
--

CREATE TABLE `assessment` (
  `id` int(20) NOT NULL,
  `element` varchar(20) NOT NULL,
  `S1` float NOT NULL,
  `S2` float NOT NULL,
  `S3` float NOT NULL,
  `S4` float NOT NULL,
  `S5` float NOT NULL,
  `userid` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `assessment`
--

INSERT INTO `assessment` (`id`, `element`, `S1`, `S2`, `S3`, `S4`, `S5`, `userid`) VALUES
(1, 'Q1', 1, 0.9, 0.7, 0.5, 0.25, 2),
(2, 'Q2', 1, 0.9, 0.8, 0.6, 0.3, 2),
(3, 'Q3', 1, 0.9, 0.8, 0.6, 0.3, 2),
(4, 'Q4', 1, 0.8, 0.5, 0.3, 0.2, 2),
(5, 'Q5', 1000, 500, 100, 10, 1, 2),
(6, 'Q6', 1000, 500, 100, 10, 1, 2),
(7, 'Q7', 1, 0.9, 0.8, 0.6, 0.3, 2),
(8, 'Q8', 1000, 500, 100, 10, 1, 2),
(9, 'Q9', 1000, 500, 100, 10, 1, 2),
(10, 'Q10', 4, 3, 2, 1, 0, 2),
(11, 'Q11', 4, 3, 2, 1, 0, 2),
(12, 'Q12', 4, 3, 2, 1, 0, 1),
(13, 'Q13', 10, 8, 6, 4, 2, 1),
(14, 'Q14', 20, 18, 16, 14, 12, 1),
(15, 'Q15', 20, 14, 10, 7, 4, 1),
(16, 'Q16', 5, 4, 3, 2, 1, 1),
(17, 'Q17', 10, 8, 6, 4, 2, 1),
(18, 'Q18', 5, 4, 3, 2, 1, 1),
(19, 'Q19', 5, 4, 3, 2, 1, 1),
(20, 'Q20', 5, 4, 3, 2, 1, 1),
(21, 'Q21', 600, 400, 200, 100, 60, 1),
(22, 'Q22', 4, 2, 1, 0.5, 0.1, 1),
(23, 'Q23', 50, 30, 20, 10, 5, 1);

-- --------------------------------------------------------

--
-- 表的结构 `config`
--

CREATE TABLE `config` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `isvisible` int(11) DEFAULT NULL,
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_time` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `config`
--

INSERT INTO `config` (`id`, `name`, `value`, `isvisible`, `created_time`, `updated_time`) VALUES
(7, 'manifold_formula', '$$ \\alpha+\\beta=\\gamma $$', 1, '2018-03-23 15:31:17', '2018-03-23 15:31:17'),
(8, 'compute_martix', '$$ \\varphi _{ \\beta }\\circ \\varphi _{ \\alpha }^{ -1 }:\\varphi _{ \\alpha }(W_{ \\alpha \\beta })\\subseteq { R}^{ m }\\mapsto \\varphi _{ \\beta }(W_{ \\alpha \\beta })\\subseteq { R }^{ m } $$', 1, '2018-03-23 15:31:17', '2018-03-23 15:31:17');

-- --------------------------------------------------------

--
-- 表的结构 `indexintro`
--

CREATE TABLE `indexintro` (
  `id` int(11) NOT NULL,
  `indexname` varchar(50) NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 DEFAULT ' ',
  `isworking` smallint(4) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `indexintro`
--

INSERT INTO `indexintro` (`id`, `indexname`, `description`, `isworking`) VALUES
(1, 'E1', ' 主机维', 0),
(2, 'E2', ' 网络维', 0),
(3, 'E3', '漏洞维 ', 0),
(4, '	Q1	', '磁盘占用率', 1),
(5, 'Q2	', 'CPU占用率', 1),
(6, '	Q3	', '内存占用率', 1),
(7, 'Q4	', '平均负载', 1),
(8, '	Q5	', '峰值流量', 1),
(9, '	Q6', '平均流量', 1),
(10, '	Q7', '带宽占用率', 1),
(11, '	Q8', '端口流量', 1),
(12, '	Q9', '网络吞吐量', 1),
(13, '	Q10', '应用漏洞个数', 1),
(14, '	Q11', '系统漏洞个数', 1),
(15, 'Q12', ' 高威胁漏洞数量', 1),
(16, 'Q13', '中等威胁漏洞数量 ', 1),
(17, 'Q14', '低等威胁漏洞数量 ', 1),
(18, 'Q15', '被扫描主机开放端口数量 ', 1),
(19, 'Q16', '关键设备漏洞个数 ', 1),
(20, 'Q17', ' 安全设备个数', 1),
(21, 'Q18', '关键设备个数 ', 1),
(22, 'Q19', '主要服务器支持的并发线程数 ', 1),
(23, 'Q20', '报警个数 ', 1),
(24, 'Q21', '关键设备平均存活时间 ', 1),
(25, 'Q22', '流量变化率 ', 1),
(26, 'Q23', '资产价值 ', 1);

-- --------------------------------------------------------

--
-- 表的结构 `indexrecord`
--

CREATE TABLE `indexrecord` (
  `id` int(11) NOT NULL,
  `nodeid` int(11) NOT NULL COMMENT '节点的id',
  `indexname` char(32) DEFAULT NULL,
  `value` double DEFAULT '1' COMMENT '表示该参数跟参考系的比值',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '观测时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `indexrecord`
--

INSERT INTO `indexrecord` (`id`, `nodeid`, `indexname`, `value`, `create_time`, `update_time`) VALUES
(5911, 1, 'Q1', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5912, 1, 'Q3', 0.2, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5913, 1, 'Q2', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5914, 1, 'Q4', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5915, 1, 'Q7', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5916, 1, 'Q6', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5917, 1, 'Q8', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5918, 1, 'Q9', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5919, 1, 'Q11', 0.54, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5920, 1, 'Q10', 0.57, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5921, 1, 'Q5', 0.2, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5922, 1, 'Q1', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5923, 1, 'Q3', 0.7, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5924, 1, 'Q2', 0.3, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5925, 1, 'Q4', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5926, 1, 'Q7', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5927, 1, 'Q6', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5928, 1, 'Q8', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5929, 1, 'Q9', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5930, 1, 'Q11', 0.37, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5931, 1, 'Q10', 0.51, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5932, 1, 'Q5', 0.7, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5933, 1, 'Q1', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:56'),
(5934, 1, 'Q3', 0.8, '2018-07-05 02:02:00', '2018-05-30 12:47:56'),
(5935, 1, 'Q2', 0.9, '2018-07-05 02:02:00', '2018-05-30 12:47:56'),
(5936, 1, 'Q4', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:56'),
(5937, 1, 'Q7', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:56'),
(5938, 1, 'Q6', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:56'),
(5939, 1, 'Q8', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:56'),
(5940, 1, 'Q9', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:56'),
(5941, 1, 'Q11', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:56'),
(5942, 1, 'Q10', 1, '2018-07-05 02:02:00', '2018-05-30 12:47:56'),
(5943, 1, 'Q5', 0.8, '2018-07-05 02:02:00', '2018-05-30 12:47:56'),
(5944, 1, 'Q1', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:56'),
(5945, 1, 'Q3', 0.3, '2018-07-05 02:03:00', '2018-05-30 12:47:56'),
(5946, 1, 'Q2', 0.2, '2018-07-05 02:03:00', '2018-05-30 12:47:56'),
(5947, 1, 'Q4', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:56'),
(5948, 1, 'Q7', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:56'),
(5949, 1, 'Q6', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:56'),
(5950, 1, 'Q8', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:56'),
(5951, 1, 'Q9', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:56'),
(5952, 1, 'Q11', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:56'),
(5953, 1, 'Q10', 1, '2018-07-05 02:03:00', '2018-05-30 12:47:56'),
(5954, 1, 'Q5', 0.3, '2018-07-05 02:03:00', '2018-05-30 12:47:56'),
(5955, 1, 'Q1', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:56'),
(5956, 1, 'Q3', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:56'),
(5957, 1, 'Q2', 0.1, '2018-07-05 02:04:00', '2018-05-30 12:47:56'),
(5958, 1, 'Q4', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:56'),
(5959, 1, 'Q7', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:56'),
(5960, 1, 'Q6', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:56'),
(5961, 1, 'Q8', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:56'),
(5962, 1, 'Q9', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:56'),
(5963, 1, 'Q11', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:56'),
(5964, 1, 'Q10', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:56'),
(5965, 1, 'Q5', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:56'),
(5966, 2, 'Q1', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5967, 2, 'Q3', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5968, 2, 'Q2', 0.3, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5969, 2, 'Q4', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5970, 2, 'Q7', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5971, 2, 'Q6', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5972, 2, 'Q8', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5973, 2, 'Q9', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5974, 2, 'Q11', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5975, 2, 'Q10', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5976, 2, 'Q5', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:56'),
(5977, 2, 'Q1', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5978, 2, 'Q3', 0.3, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5979, 2, 'Q2', 0.8, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5980, 2, 'Q4', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5981, 2, 'Q7', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5982, 2, 'Q6', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:56'),
(5983, 2, 'Q8', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(5984, 2, 'Q9', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(5985, 2, 'Q11', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(5986, 2, 'Q10', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(5987, 2, 'Q5', 0.3, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(5988, 2, 'Q1', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(5989, 2, 'Q3', 0.9, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(5990, 2, 'Q2', 0.9, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(5991, 2, 'Q4', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(5992, 2, 'Q7', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(5993, 2, 'Q6', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(5994, 2, 'Q8', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(5995, 2, 'Q9', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(5996, 2, 'Q11', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(5997, 2, 'Q10', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(5998, 2, 'Q5', 0.9, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(5999, 2, 'Q1', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6000, 2, 'Q3', 0.2, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6001, 2, 'Q2', 0.2, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6002, 2, 'Q4', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6003, 2, 'Q7', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6004, 2, 'Q6', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6005, 2, 'Q8', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6006, 2, 'Q9', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6007, 2, 'Q11', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6008, 2, 'Q10', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6009, 2, 'Q5', 0.2, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6010, 2, 'Q1', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6011, 2, 'Q3', 0.1, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6012, 2, 'Q2', 0.1, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6013, 2, 'Q4', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6014, 2, 'Q7', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6015, 2, 'Q6', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6016, 2, 'Q8', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6017, 2, 'Q9', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6018, 2, 'Q11', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6019, 2, 'Q10', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6020, 2, 'Q5', 0.1, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6021, 3, 'Q1', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:57'),
(6022, 3, 'Q3', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:57'),
(6023, 3, 'Q2', 0.2, '2018-07-05 02:00:00', '2018-05-30 12:47:57'),
(6024, 3, 'Q4', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:57'),
(6025, 3, 'Q7', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:57'),
(6026, 3, 'Q6', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:57'),
(6027, 3, 'Q8', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:57'),
(6028, 3, 'Q9', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:57'),
(6029, 3, 'Q11', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:57'),
(6030, 3, 'Q10', 0, '2018-07-05 02:00:00', '2018-05-30 12:47:57'),
(6031, 3, 'Q5', 0.2, '2018-07-05 02:00:00', '2018-05-30 12:47:57'),
(6032, 3, 'Q1', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(6033, 3, 'Q3', 0.3, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(6034, 3, 'Q2', 0.7, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(6035, 3, 'Q4', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(6036, 3, 'Q7', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(6037, 3, 'Q6', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(6038, 3, 'Q8', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(6039, 3, 'Q9', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(6040, 3, 'Q11', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(6041, 3, 'Q10', 0, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(6042, 3, 'Q5', 0.7, '2018-07-05 02:01:00', '2018-05-30 12:47:57'),
(6043, 3, 'Q1', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(6044, 3, 'Q3', 0.9, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(6045, 3, 'Q2', 0.8, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(6046, 3, 'Q4', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(6047, 3, 'Q7', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(6048, 3, 'Q6', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(6049, 3, 'Q8', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(6050, 3, 'Q9', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(6051, 3, 'Q11', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(6052, 3, 'Q10', 0, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(6053, 3, 'Q5', 0.8, '2018-07-05 02:02:00', '2018-05-30 12:47:57'),
(6054, 3, 'Q1', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6055, 3, 'Q3', 0.2, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6056, 3, 'Q2', 0.3, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6057, 3, 'Q4', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6058, 3, 'Q7', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6059, 3, 'Q6', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6060, 3, 'Q8', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6061, 3, 'Q9', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6062, 3, 'Q11', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6063, 3, 'Q10', 0, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6064, 3, 'Q5', 0.3, '2018-07-05 02:03:00', '2018-05-30 12:47:57'),
(6065, 3, 'Q1', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6066, 3, 'Q3', 0.1, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6067, 3, 'Q2', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6068, 3, 'Q4', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6069, 3, 'Q7', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6070, 3, 'Q6', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6071, 3, 'Q8', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6072, 3, 'Q9', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6073, 3, 'Q11', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6074, 3, 'Q10', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57'),
(6075, 3, 'Q5', 0, '2018-07-05 02:04:00', '2018-05-30 12:47:57');

-- --------------------------------------------------------

--
-- 表的结构 `menu`
--

CREATE TABLE `menu` (
  `id` int(11) NOT NULL,
  `path` varchar(255) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `sortid` int(11) NOT NULL,
  `page` varchar(255) DEFAULT NULL,
  `parentid` int(11) DEFAULT NULL,
  `imgurl` varchar(255) DEFAULT NULL,
  `isvisible` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `menu`
--

INSERT INTO `menu` (`id`, `path`, `name`, `sortid`, `page`, `parentid`, `imgurl`, `isvisible`) VALUES
(1, '/', '首页', 100, 'index.html', -1, 'icon icon-home icon-fw', 0),
(2, 'login', '登录', 900, 'login.html', -1, NULL, 0),
(3, 'manifold', '流形计算', 300, 'manifold_show.html', -1, 'icon-certificate', 1),
(4, 'config', '配置参数', 600, 'config.html', -1, 'icon-cogs', 1),
(5, 'output', '导出结果', 700, 'output.html', -1, 'icon-download', 0),
(6, 'input', '输入数据', 200, 'input.html', -1, 'icon-upload', 1),
(7, 'ahp', 'AHP计算', 400, 'ahp.html', -1, 'icon-sitemap', 1),
(8, 'test', '测试', 800, 'test.html', -1, 'icon-gavel ', 0),
(9, 'd3mhl', '多层多维多粒度', 500, 'd3mhl.html', -1, 'icon-reorder', 1),
(10, 'templatecreate', '模板创建', 150, 'templatecreate.html', -1, 'icon-cogs', 1);

-- --------------------------------------------------------

--
-- 表的结构 `nodeindex`
--

CREATE TABLE `nodeindex` (
  `id` int(11) NOT NULL,
  `nodeid` int(11) NOT NULL COMMENT '节点的id',
  `nodeTypeid` int(11) NOT NULL,
  `create_time` timestamp NULL DEFAULT NULL COMMENT '观测时间',
  `importance` varchar(32) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `nodeindex`
--

INSERT INTO `nodeindex` (`id`, `nodeid`, `nodeTypeid`, `create_time`, `importance`) VALUES
(511, 1, 3, '2018-07-05 02:00:00', '0.4'),
(512, 1, 3, '2018-07-05 02:01:00', '0.4'),
(513, 1, 3, '2018-07-05 02:02:00', '0.4'),
(514, 1, 3, '2018-07-05 02:03:00', '0.4'),
(515, 1, 3, '2018-07-05 02:04:00', '0.4'),
(516, 2, 1, '2018-07-05 02:00:00', '0.78'),
(517, 2, 1, '2018-07-05 02:01:00', '0.78'),
(518, 2, 1, '2018-07-05 02:02:00', '0.78'),
(519, 2, 1, '2018-07-05 02:03:00', '0.78'),
(520, 2, 1, '2018-07-05 02:04:00', '0.78'),
(521, 3, 6, '2018-07-05 02:00:00', '0.75'),
(522, 3, 6, '2018-07-05 02:01:00', '0.75'),
(523, 3, 6, '2018-07-05 02:02:00', '0.75'),
(524, 3, 6, '2018-07-05 02:03:00', '0.75'),
(525, 3, 6, '2018-07-05 02:04:00', '0.75');

-- --------------------------------------------------------

--
-- 表的结构 `noderelates`
--

CREATE TABLE `noderelates` (
  `id` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `cid` int(11) NOT NULL,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `importance` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `noderelates`
--

INSERT INTO `noderelates` (`id`, `pid`, `cid`, `update_time`, `importance`) VALUES
(1, 1, 2, '2018-07-05 02:00:00', '0.9'),
(2, 1, 2, '2018-07-05 02:01:00', '0.7'),
(3, 1, 2, '2018-07-05 02:02:00', '0.4'),
(4, 1, 2, '2018-07-05 02:03:00', '0.6'),
(5, 1, 2, '2018-07-05 02:04:00', '0.4'),
(6, 2, 3, '2018-07-05 02:00:00', '0.8'),
(7, 2, 3, '2018-07-05 02:01:00', '0.6'),
(8, 2, 3, '2018-07-05 02:02:00', '0.5'),
(9, 2, 3, '2018-07-05 02:03:00', '0.7'),
(10, 2, 3, '2018-07-05 02:04:00', '0.6');

-- --------------------------------------------------------

--
-- 表的结构 `nodetype`
--

CREATE TABLE `nodetype` (
  `id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `imgurl` varchar(255) DEFAULT NULL,
  `userid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `nodetype`
--

INSERT INTO `nodetype` (`id`, `name`, `imgurl`, `userid`) VALUES
(1, '路由器', 'static/object/router.jpg.png', 1),
(2, '防火墙', 'static/object/firewall.jpg', 1),
(3, '交换机', 'static/object/switch.jpg.png', 1),
(4, '容器', 'static/object/computer.png', 1),
(5, '服务器', 'static/object/computer.png', 1),
(6, '主机', 'static/object/cloud.png', 1),
(7, 'A', '', 1),
(8, 'B', '', 1),
(9, 'C', NULL, 1);

-- --------------------------------------------------------

--
-- 表的结构 `node_ser`
--

CREATE TABLE `node_ser` (
  `id` int(11) NOT NULL,
  `nodeid` int(11) NOT NULL,
  `serviceid` int(11) NOT NULL,
  `importance` double NOT NULL DEFAULT '0.5',
  `port` int(11) NOT NULL COMMENT '端口号'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `node_ser`
--

INSERT INTO `node_ser` (`id`, `nodeid`, `serviceid`, `importance`, `port`) VALUES
(73, 1, 1, 0.1, 80),
(74, 1, 2, 0.2, 8080),
(75, 1, 3, 0.3, 443),
(76, 1, 4, 0.4, 3306),
(77, 2, 2, 0.5, 8000),
(78, 2, 3, 0, 22),
(79, 2, 4, 0.6, 80),
(80, 2, 5, 0.7, 443),
(81, 2, 6, 0.24, 8080),
(82, 3, 1, 0.46, 9000),
(83, 3, 2, 0.38, 3306),
(84, 3, 3, 0.21, 80),
(85, 3, 4, 0.35, 22),
(86, 3, 5, 0.67, 443),
(87, 3, 6, 0.89, 8000);

-- --------------------------------------------------------

--
-- 表的结构 `node_vul`
--

CREATE TABLE `node_vul` (
  `id` int(11) NOT NULL,
  `nodeid` int(11) NOT NULL,
  `vulid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `node_vul`
--

INSERT INTO `node_vul` (`id`, `nodeid`, `vulid`) VALUES
(68, 1, 2),
(69, 1, 3),
(70, 1, 5),
(71, 1, 6),
(72, 2, 1),
(73, 2, 2),
(74, 2, 3),
(75, 2, 4),
(76, 3, 3),
(77, 3, 6),
(78, 3, 10),
(79, 3, 15),
(80, 3, 18);

-- --------------------------------------------------------

--
-- 表的结构 `servicetype`
--

CREATE TABLE `servicetype` (
  `id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `userid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `servicetype`
--

INSERT INTO `servicetype` (`id`, `name`, `userid`) VALUES
(1, 'HTTP ', 1),
(2, 'TELNET', 1),
(3, 'FTP ', 1),
(4, 'DNS ', 1),
(5, 'SSH', 1),
(6, 'TELNET', 1);

-- --------------------------------------------------------

--
-- 表的结构 `sheet`
--

CREATE TABLE `sheet` (
  `id` int(11) NOT NULL,
  `sheetname` varchar(50) NOT NULL,
  `colname` varchar(250) NOT NULL,
  `tempid` int(11) NOT NULL,
  `sortid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `sheet`
--

INSERT INTO `sheet` (`id`, `sheetname`, `colname`, `tempid`, `sortid`) VALUES
(1, 'node_service', 'nodeid', 1, 10),
(2, 'node_service', 'serviceid', 1, 20),
(3, 'node_service', 'importance', 1, 30),
(4, 'judgementmatrix', 'id', 1, 10),
(5, 'judgementmatrix', 'pid', 1, 20),
(6, 'judgementmatrix', 'cid', 1, 30),
(7, 'judgementmatrix', 'value', 1, 40),
(8, 'node_vul', 'nodeid', 1, 10),
(9, 'node_vul', 'vulid', 1, 20),
(10, 'node', 'id', 1, 10),
(11, 'node', 'nodetype', 1, 20),
(12, 'node', 'importance', 1, 30),
(13, 'node', 'service', 1, 40),
(14, 'node', 'serviceimportance', 1, 50),
(15, 'node', 'updatetime', 1, 60),
(16, 'links', 'id', 1, 10),
(17, 'links', 'source', 1, 20),
(18, 'links', 'target', 1, 30),
(19, 'links', 'importance', 1, 40),
(20, 'links', 'updatetime', 1, 50),
(21, 'node_service', 'port', 1, 40);

-- --------------------------------------------------------

--
-- 表的结构 `template`
--

CREATE TABLE `template` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `size` int(11) NOT NULL,
  `path` varchar(255) NOT NULL,
  `isworking` tinyint(4) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `template`
--

INSERT INTO `template` (`id`, `name`, `size`, `path`, `isworking`) VALUES
(1, 'emptyemplate', 0, 'emptytemplate.xlsx', 1),
(6, '学校教育网模板', 30, '学校教育网模板20180518112637.xls', 1),
(7, '企业内部网络模板', 100, '企业内部网络模板20180518113551.xls', 1),
(8, '政府机构网络模板', 100, '政府机构网络模板20180518114241.xls', 1),
(9, '企业对外网络模板', 30, '企业对外网络模板20180518114653.xls', 1),
(14, '家庭网络', 3, '家庭网络201805291835.xlsx', 1),
(15, '校园网络', 10, '校园网络201805301851.xlsx', 1);

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(80) DEFAULT NULL,
  `email` varchar(320) DEFAULT NULL,
  `phone` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `phone`) VALUES
(1, 'itmin', '1608500576@qq.com', '17801071701'),
(2, '123', '1231212313', '21311321311');

-- --------------------------------------------------------

--
-- 表的结构 `vulnerability`
--

CREATE TABLE `vulnerability` (
  `id` int(11) NOT NULL COMMENT '主键',
  `name` varchar(60) NOT NULL COMMENT '名字',
  `v2score` varchar(60) NOT NULL COMMENT 'CVSS2漏洞评分',
  `v3score` varchar(60) NOT NULL COMMENT 'CVSS2漏洞评分'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `vulnerability`
--

INSERT INTO `vulnerability` (`id`, `name`, `v2score`, `v3score`) VALUES
(1, 'XSS', '4.3', '6.1'),
(2, 'SQL Injection', '5.5', '6.4'),
(3, 'POODLE', '4.3', '3.1'),
(4, 'Dos', '9.0', '9.9'),
(5, 'XML Parser', '4.6', '4.2'),
(6, 'AAA authorization', '8.5', '8.8'),
(7, 'iWork Denail of Service', '6.8', '7.8'),
(8, 'OpenSSL', '5.0', '7.5'),
(9, 'Bash \'Shellhock\'', '10.0', '9.8'),
(10, 'DNS Kaminsky Bug', '5.0', '6.8'),
(11, 'Sophos Login Screen Bypass', '6.9', '6.8'),
(12, 'Joomla Directory Traversal', '5.0', '5.8'),
(13, 'Cisco Access Control Bypass', '5.0', '5.8'),
(14, 'Juniper Proxy ARP Denial of Service', '6.1', '9.3'),
(15, 'DokuWiki Reflected Cross-site Scripting Attack', '4.3', '5.4'),
(16, 'Adobe Acrobat Buffer Overflow', '9.3', '7.8'),
(17, 'Microsoft Windows Bluetooth Remote Code Execution', '8.3', '8.8'),
(18, 'Apple iOS Security Control Bypass', '4.9', '4.6'),
(19, 'SearchBlox Cross-Site Request Forgery', '6.8', '8.8'),
(20, 'SSL/TLS MITM', '6.8', '7.4'),
(21, 'Google Chrome Sandbox Bypass', '10.0', '9.6'),
(22, 'SAMR/LSAD Privilege Escalation via Protocol Downgrade', '5.8', '7.5');

--
-- 转储表的索引
--

--
-- 表的索引 `ahpjudgement`
--
ALTER TABLE `ahpjudgement`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- 表的索引 `ahp_tree`
--
ALTER TABLE `ahp_tree`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `assessment`
--
ALTER TABLE `assessment`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `config`
--
ALTER TABLE `config`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- 表的索引 `indexintro`
--
ALTER TABLE `indexintro`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `indexrecord`
--
ALTER TABLE `indexrecord`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `nodeindex`
--
ALTER TABLE `nodeindex`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `noderelates`
--
ALTER TABLE `noderelates`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `nodetype`
--
ALTER TABLE `nodetype`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `node_ser`
--
ALTER TABLE `node_ser`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK2` (`serviceid`);

--
-- 表的索引 `node_vul`
--
ALTER TABLE `node_vul`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_node_vul2` (`vulid`);

--
-- 表的索引 `servicetype`
--
ALTER TABLE `servicetype`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `sheet`
--
ALTER TABLE `sheet`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `template`
--
ALTER TABLE `template`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- 表的索引 `vulnerability`
--
ALTER TABLE `vulnerability`
  ADD UNIQUE KEY `id` (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `ahpjudgement`
--
ALTER TABLE `ahpjudgement`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=556;

--
-- 使用表AUTO_INCREMENT `ahp_tree`
--
ALTER TABLE `ahp_tree`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- 使用表AUTO_INCREMENT `assessment`
--
ALTER TABLE `assessment`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- 使用表AUTO_INCREMENT `config`
--
ALTER TABLE `config`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- 使用表AUTO_INCREMENT `indexintro`
--
ALTER TABLE `indexintro`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- 使用表AUTO_INCREMENT `indexrecord`
--
ALTER TABLE `indexrecord`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6076;

--
-- 使用表AUTO_INCREMENT `menu`
--
ALTER TABLE `menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- 使用表AUTO_INCREMENT `nodeindex`
--
ALTER TABLE `nodeindex`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=526;

--
-- 使用表AUTO_INCREMENT `noderelates`
--
ALTER TABLE `noderelates`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- 使用表AUTO_INCREMENT `nodetype`
--
ALTER TABLE `nodetype`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- 使用表AUTO_INCREMENT `node_ser`
--
ALTER TABLE `node_ser`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=88;

--
-- 使用表AUTO_INCREMENT `node_vul`
--
ALTER TABLE `node_vul`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- 使用表AUTO_INCREMENT `servicetype`
--
ALTER TABLE `servicetype`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- 使用表AUTO_INCREMENT `sheet`
--
ALTER TABLE `sheet`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- 使用表AUTO_INCREMENT `template`
--
ALTER TABLE `template`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- 使用表AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `vulnerability`
--
ALTER TABLE `vulnerability`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键', AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
