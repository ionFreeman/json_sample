package edu.pace.seidenberg.dps2020.team2

import java.io.{BufferedInputStream, BufferedReader, InputStreamReader}

import org.apache.http.client.methods.{HttpGet, HttpPost}
import org.apache.http.entity.StringEntity
import org.apache.http.impl.client.HttpClientBuilder
import play.api.libs.json._
import org.slf4j.LoggerFactory

import scala.io.Source

case class JsonSample(url: String = "localhost:5000/contactdb") {
  val builder = HttpClientBuilder.create()
  val logger = LoggerFactory.getLogger(this.getClass)

  /**
    *
    * @return the JSON response body from a GET as a string
    */
  def getJson(dummyArg:Int):String = {
    val content = new BufferedReader(
      new InputStreamReader(
        builder.build.execute(
          new HttpGet(url)).getEntity.getContent)).lines.toArray mkString "\n"
    logger.info(s"$content")
    content
  }

  /**
    * Sequentially posts the stream members to the POST URL
    * @param contacts a stream of contact defining dicts. Each must define lname and fname.
    * @return the last response
    */
  def postJson(contacts: Stream[Map[String, String]]): String = {
    val contents = for {contact <- contacts}
      yield {
        val post = new HttpPost(url)
        post.setHeader("Content-Type", "application/json")
        val ent = new StringEntity(Json.stringify(Json.toJson(contact)), "UTF-8")
        post.setEntity(ent)
        val httpResponse = builder.build.execute(post)
        val inputStream = httpResponse.getEntity().getContent()
        val content = Source.fromInputStream(inputStream).getLines.mkString("\n")
        inputStream.close
        content
      }
    contents.last
  }
}

