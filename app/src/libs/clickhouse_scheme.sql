CREATE DATABASE IF NOT EXISTS analytics;

 CREATE TABLE `analytics`.`visit_stat_queue` (
  `timestamp` UInt64,
  `project` String,
  `path` String,
  `request_ip` String,
  `user_agent` String
  ) ENGINE = Kafka('kafka_analytics:9092', 'visit_stat_topic', 'group_1', 'JSONEachRow');

CREATE TABLE `analytics`.`visit_stat` (
  `uid` UUID,
  `date_visit` Date,
  `time_visit` DateTime,
  `timestamp` UInt64,
  `project` String,
  `path` String,
  `request_ip` String,
  `user_agent` String
) ENGINE = MergeTree(date_visit, (date_visit, path), 8192);

CREATE MATERIALIZED VIEW `analytics`.`visit_stat_consumer` TO `analytics`.`visit_stat`
    AS SELECT toUUID(rand64()) as `uid`, toDate(toDateTime(`timestamp`)) AS `date_visit`, toDateTime(`timestamp`) as `time_visit`, `timestamp`, `project`, `path`, `request_ip`, `user_agent`
    FROM `analytics`.`visit_stat_queue`;


-- SELECT * FROM `analytics`.`visit_stat_queue`;
-- SELECT * FROM `analytics`.`visit_stat`;

SELECT toUUID(rand64());