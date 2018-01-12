import org.apache.spark.sql.types._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.SparkSession
import java.nio.file.Paths

object ETL {
  def main(args: Array[String]) {
    val giftPath = args(0)
    val inRepo = args(1)
    val destRepo = args(2)
    val date = args(3)

    val format = new java.text.SimpleDateFormat("yyyy_MM_dd")
    val today = format.parse(date).getDate

    val spark = SparkSession
      .builder()
      .appName("Danmu ETL " + date)
      .getOrCreate()

    import spark.implicits._

    val danmuSchema = StructType(Array(
      StructField("room", IntegerType, nullable = true),
      StructField("user", IntegerType, nullable = true),
      StructField("ts", IntegerType, nullable = true)
    ))

    val giftPriceSchema = StructType(Array(
      StructField("gift", StringType, nullable = true),
      StructField("gid", IntegerType, nullable = true),
      StructField("price", IntegerType, nullable = true)
    ))

    val giftSchema = StructType(Array(
      StructField("room", IntegerType, nullable = true),
      StructField("user", IntegerType, nullable = true),
      StructField("ts", IntegerType, nullable = true),
      StructField("gift", IntegerType, nullable = true)
    ))

    val danmuDF = spark.read.format("csv")
      .schema(danmuSchema)
      .option("sep", "\t")
      .option("header", value = true)
      .load(Paths.get(inRepo, date + "_text.txt").toString)
      .select($"user", $"room", hour(from_unixtime($"ts")).as("hour"))
      .filter(dayofmonth(from_unixtime($"ts")) === today)

    val giftDF = spark.read.format("csv")
      .schema(giftSchema)
      .option("sep", "\t")
      .option("header", value = true)
      .load(Paths.get(inRepo, date + "_gift.txt").toString)
      .select($"user", $"room", $"gift", hour(from_unixtime($"ts")).as("hour"))
      .filter(dayofmonth(from_unixtime($"ts")) === today)


    val giftPriceDF = spark.read.format("csv")
      .schema(giftPriceSchema)
      .option("sep", "\t")
      .option("header", value = true)
      .load(giftPath)


    danmuDF.createTempView("danmu")
    giftDF.createTempView("gift")
    giftPriceDF.createTempView("giftPrice")

    val danmuUserDF = spark.sql("SELECT user, room, hour, COUNT(*) AS dcount FROM danmu GROUP BY user, room, hour")

    val giftUserDF = spark.sql("SELECT user, room, hour, COUNT(*) AS gcount, SUM(gp.price) AS expense " +
      "FROM gift AS g JOIN giftPrice AS gp ON g.gift = gp.gid " +
      "GROUP BY user, room, hour")

    danmuUserDF.createOrReplaceTempView("danmu")
    giftUserDF.createOrReplaceTempView("gift")

    val joinedDF = spark.sql("SELECT " +
      "IF(d.user IS NULL, g.user, d.user) AS user, " +
      "IF(d.room IS NULL, g.room, d.room) AS room, " +
      "IF(d.hour IS NULL, g.hour, d.hour) AS hour, " +
      "IF(dcount IS NULL, 0, dcount) AS dc, " +
      "IF(gcount IS NULL, 0, gcount) AS gc, " +
      "IF(expense IS NULL, 0, expense) AS exp " +
      "FROM danmu AS d " +
      "FULL JOIN gift AS g ON d.user = g.user AND d.room = g.room AND d.hour = g.hour")

    joinedDF.persist()

    joinedDF.coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_user_room_hourly").toString)


    joinedDF.createOrReplaceTempView("combined")

    spark.sql("SELECT * FROM " +
      "(SELECT room, user, " +
      "SUM(dc) AS dcount, SUM(gc) AS gcount, SUM(exp) AS expense, ROW_NUMBER() OVER (PARTITION BY room ORDER BY SUM(exp) DESC) AS rn " +
      "FROM combined GROUP BY room, user) AS t " +
      "WHERE rn <= 20")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_room_top_user_daily_order_by_expense").toString)

    spark.sql("SELECT * FROM " +
      "(SELECT room, user, " +
      "SUM(dc) AS dcount, SUM(gc) AS gcount, SUM(exp) AS expense, ROW_NUMBER() OVER (PARTITION BY room ORDER BY SUM(gc) DESC) AS rn " +
      "FROM combined GROUP BY room, user) AS t " +
      "WHERE rn <= 20")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_room_top_user_daily_order_by_gcount").toString)

    spark.sql("SELECT * FROM " +
      "(SELECT room, user, " +
      "SUM(dc) AS dcount, SUM(gc) AS gcount, SUM(exp) AS expense, ROW_NUMBER() OVER (PARTITION BY room ORDER BY SUM(dc) DESC) AS rn " +
      "FROM combined GROUP BY room, user) AS t " +
      "WHERE rn <= 20")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_room_top_user_daily_order_by_dcount").toString)

    spark.sql("SELECT user, " +
      "SUM(dc) AS dcount, SUM(gc) AS gcount, SUM(exp) AS expense " +
      "FROM combined GROUP BY user ORDER BY expense DESC LIMIT 20")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_site_top_user_daily_order_by_expense").toString)

    spark.sql("SELECT user, " +
      "SUM(dc) AS dcount, SUM(gc) AS gcount, SUM(exp) AS expense " +
      "FROM combined GROUP BY user ORDER BY gcount DESC LIMIT 20")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_site_top_user_daily_order_by_gcount").toString)

    spark.sql("SELECT user, " +
      "SUM(dc) AS dcount, SUM(gc) AS gcount, SUM(exp) AS expense " +
      "FROM combined GROUP BY user ORDER BY dcount DESC LIMIT 20")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_site_top_user_daily_order_by_dcount").toString)

    spark.sql("SELECT room, hour, " +
      "COUNT(DISTINCT(user)) AS ucount, " +
      "COUNT(DISTINCT(CASE WHEN dc>0 THEN user END)) AS ducount, " +
      "COUNT(DISTINCT(CASE WHEN gc>0 THEN user END)) AS gucount, " +
      "SUM(dc) AS dcount, SUM(gc) AS gcount, SUM(exp) AS income " +
      "FROM combined GROUP BY room, hour")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_room_hourly").toString)

    spark.sql("SELECT room, " +
      "COUNT(DISTINCT(user)) AS ucount, " +
      "COUNT(DISTINCT(CASE WHEN dc>0 THEN user END)) AS ducount, " +
      "COUNT(DISTINCT(CASE WHEN gc>0 THEN user END)) AS gucount, " +
      "SUM(dc) AS dcount, SUM(gc) AS gcount, SUM(exp) AS income " +
      "FROM combined GROUP BY room")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_room_daily").toString)

    spark.sql("SELECT hour, " +
      "COUNT(DISTINCT(user)) AS ucount, " +
      "COUNT(DISTINCT(CASE WHEN dc>0 THEN user END)) AS ducount, " +
      "COUNT(DISTINCT(CASE WHEN gc>0 THEN user END)) AS gucount, " +
      "SUM(dc) AS dcount, SUM(gc) AS gcount, SUM(exp) AS income " +
      "FROM combined GROUP BY hour")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_site_hourly").toString)

    spark.sql("SELECT " +
      "COUNT(DISTINCT(user)) AS ucount, " +
      "COUNT(DISTINCT(CASE WHEN dc>0 THEN user END)) AS ducount, " +
      "COUNT(DISTINCT(CASE WHEN gc>0 THEN user END)) AS gucount, " +
      "SUM(dc) AS dcount, SUM(gc) AS gcount, SUM(exp) AS income " +
      "FROM combined")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_site_daily").toString)
  }
}
