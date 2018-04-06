CREATE EXTERNAL TABLE record (uid INT, rid INT, hour INT, dc INT, gc INT, exp BIGINT) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/data/douyu/'
TBLPROPERTIES ("skip.header.line.count"="1");

SELECT a.rid, b.rid, COUNT(DISTINCT a.uid) AS c
FROM (
	SELECT t2.*
    FROM
        ( SELECT rid, COUNT(DISTINCT uid) AS users
          FROM record
          GROUP BY rid
          ORDER BY users DESC
          LIMIT 100
        ) AS t1
    INNER JOIN record AS t2 ON t1.rid = t2.rid
) AS a
INNER JOIN (
    SELECT t4.*
    FROM
        ( SELECT rid, COUNT(DISTINCT uid) AS users
          FROM record
          GROUP BY rid
          ORDER BY users DESC
          LIMIT 100
        ) AS t3
    INNER JOIN record AS t4 ON t3.rid = t4.rid
) AS b 
ON a.uid = b.uid
WHERE a.rid != b.rid
GROUP BY a.rid, b.rid
ORDER BY a.rid, c DESC;
