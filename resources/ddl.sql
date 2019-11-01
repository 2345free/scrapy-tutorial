CREATE TABLE `quotes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(2048) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `author` varchar(50) COLLATE utf8_bin NOT NULL,
  `tags` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;