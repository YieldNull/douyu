import org.apache.spark.sql.types._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.SparkSession
import java.nio.file.Paths

object ETL {
  def main(args: Array[String]) {
    val giftModelPath = args(0)
    val inRepo = args(1)
    val destRepo = args(2)
    val date = args(3)

    val format = new java.text.SimpleDateFormat("yyyy_MM_dd")
    val day = format.parse(date).getDate

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
      .select($"user", $"room", from_unixtime($"ts").as("uts"))
      .select($"user", $"room",
        year($"uts").as("year"),
        month($"uts").as("month"),
        dayofmonth($"uts").as("day"),
        hour($"uts").as("hour")
      ).filter($"day" === day)


    val giftDF = spark.read.format("csv")
      .schema(giftSchema)
      .option("sep", "\t")
      .option("header", value = true)
      .load(Paths.get(inRepo, date + "_gift.txt").toString)
      .select($"user", $"room", $"gift", from_unixtime($"ts").as("uts"))
      .select($"user", $"room", $"gift",
        year($"uts").as("year"),
        month($"uts").as("month"),
        dayofmonth($"uts").as("day"),
        hour($"uts").as("hour")
      ).filter($"day" === day)


    val giftPriceDF = spark.read.format("csv")
      .schema(giftPriceSchema)
      .option("sep", "\t")
      .option("header", value = true)
      .load(giftModelPath)


    danmuDF.createTempView("danmu")
    giftDF.createTempView("gift")
    giftPriceDF.createTempView("giftPrice")

    danmuDF.persist()
    giftPriceDF.persist()
    giftDF.persist()

    spark.sql("SELECT user, room, year, month, day, hour, COUNT(*) AS count " +
      "FROM danmu GROUP BY user, room, year, month, day, hour")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_count_danmu_groupby_user_room_hourly").toString)

    spark.sql("SELECT user, room, year, month, day, hour, COUNT(*) AS count, SUM(gp.price) AS expense " +
      "FROM gift JOIN giftPrice AS gp ON gift.gift = gp.gid " +
      "GROUP BY user, room, year, month, day, hour")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_count_gift_groupby_user_room_hourly").toString)

    spark.sql("SELECT room, year, month, day, hour, COUNT(*) AS count, COUNT(DISTINCT(user)) AS ucount " +
      "FROM danmu GROUP BY room, year, month, day, hour")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_count_danmu_user_groupby_room_hourly").toString)

    spark.sql("SELECT room, year, month, day, COUNT(*) AS count, COUNT(DISTINCT(user)) AS ucount " +
      "FROM danmu GROUP BY room, year, month, day")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_count_danmu_user_groupby_room_daily").toString)

    spark.sql("SELECT room, year, month, day, hour, COUNT(DISTINCT(user)) AS ucount, COUNT(*) AS gcount, SUM(gp.price) AS income " +
      "FROM gift JOIN giftPrice AS gp ON gift.gift = gp.gid " +
      "GROUP BY room, year, month, day, hour")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_count_gift_user_groupby_room_hourly").toString)

    spark.sql("SELECT room, year, month, day, COUNT(DISTINCT(user)) AS ucount, COUNT(*) AS gcount, SUM(gp.price) AS income " +
      "FROM gift JOIN giftPrice AS gp ON gift.gift = gp.gid " +
      "GROUP BY room, year, month, day")
      .coalesce(1).write.format("csv").option("header", value = true)
      .save(Paths.get(destRepo, date + "_count_gift_user_groupby_room_daily").toString)
  }
}
