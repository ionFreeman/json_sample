import edu.pace.seidenberg.dps2020.team2.JsonSample
import org.slf4j.{Logger, LoggerFactory}

val logger = LoggerFactory.getLogger("json_sample")
val jsonSample = JsonSample("http://localhost:5000/contactdb")
jsonSample.postJson(Stream(
  Map("fname" -> "Ion", "lname" -> "Freeman")
  // Vladimir Putin and Mohandas Gandhi to show off Unicode
, Map("fname" -> "Влади́мир", "lname" -> "Пу́тин")
, Map("fname" -> "मोहनदास", "lname" -> "गांधी")))

val db = jsonSample.getJson(0)
logger.info(s"contact database:\n$db")


