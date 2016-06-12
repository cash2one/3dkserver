ALTER TABLE `tb_character` CHANGE COLUMN `lead_id` `lead_id` INT(10) UNSIGNED NOT NULL DEFAULT '1'  , CHANGE COLUMN `level` `level` INT(10) UNSIGNED NOT NULL DEFAULT '1'  , CHANGE COLUMN `exp` `exp` INT(10) UNSIGNED NOT NULL DEFAULT '0'  , CHANGE COLUMN `vip_level` `vip_level` INT(10) UNSIGNED NOT NULL DEFAULT '0'  , CHANGE COLUMN `might` `might` INT(10) UNSIGNED NOT NULL DEFAULT '0'  , CHANGE COLUMN `golds` `golds` INT(10) UNSIGNED NOT NULL DEFAULT '0'  , CHANGE COLUMN `credits` `credits` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0'  , CHANGE COLUMN `fellow_capacity` `fellow_capacity` SMALLINT(6) UNSIGNED NOT NULL DEFAULT '0'  , CHANGE COLUMN `item_capacity` `item_capacity` SMALLINT(6) UNSIGNED NOT NULL DEFAULT '0'  , CHANGE COLUMN `treasure_capacity` `treasure_capacity` SMALLINT(6) UNSIGNED NOT NULL DEFAULT '0'  , CHANGE COLUMN `equip_capacity` `equip_capacity` SMALLINT(6) UNSIGNED NOT NULL DEFAULT '0'  , CHANGE COLUMN `equipshard_capacity` `equipshard_capacity` SMALLINT(6) UNSIGNED NOT NULL DEFAULT '0'  , CHANGE COLUMN `credits_payed` `credits_payed` INT(11) UNSIGNED NULL DEFAULT '0'  , CHANGE COLUMN `register_time` `register_time` INT(10) UNSIGNED NOT NULL DEFAULT '0'  , CHANGE COLUMN `soul` `soul` INT(10) UNSIGNED NULL DEFAULT '0'  , ADD COLUMN `hunyu` INT(10) UNSIGNED NULL DEFAULT 0  AFTER `soul` ;

ALTER TABLE `tb_bag_equip` ADD COLUMN `refine_cost` INT(10) UNSIGNED NULL DEFAULT 0  AFTER `strengthen_cost` ;

