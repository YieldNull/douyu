package cn.edu.zju.douyu.mq;

import cn.edu.zju.douyu.emot.Emotion;
import com.alibaba.fastjson.JSONObject;
import com.rabbitmq.client.*;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class LiveParser {

    static class StreamProducer {
        final static String EXCHANGE = "amq.topic";
        final static String ROUTE_STREAM = "stream.room.";

        Connection connection;
        Channel channel;

        public StreamProducer() throws IOException, TimeoutException {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");
            connection = factory.newConnection();

            channel = connection.createChannel();
        }

        public void produce(String route, String msg) throws IOException {
            channel.basicPublish(EXCHANGE, route, null, msg.getBytes());
        }
    }

    static class EmotConsumer {
        final static String QUEUE_NAME = "danmu.queue.emot";
        final static String EXCHANGE_NAME = "danmu.emot";
        final static String ROUTE_PARSER = "parser";

        Connection connection;
        Channel channel;

        public EmotConsumer() throws IOException, TimeoutException {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");
            connection = factory.newConnection();

            channel = connection.createChannel();

            channel.exchangeDeclare(EXCHANGE_NAME, BuiltinExchangeType.DIRECT);
            channel.queueDeclare(QUEUE_NAME, false, false, false, null);
            channel.queueBind(QUEUE_NAME, EXCHANGE_NAME, ROUTE_PARSER);
        }

        public void consume(final StreamProducer producer) throws IOException {
            Consumer consumer = new DefaultConsumer(channel) {
                Emotion emotion = new Emotion();

                @Override
                public void handleDelivery(String consumerTag, Envelope envelope,
                                           AMQP.BasicProperties properties, byte[] body)
                        throws IOException {
                    String message = new String(body, "UTF-8");


                    JSONObject obj = JSONObject.parseObject(message);
                    String content = obj.getString("content");

                    if (content != null) {
                        double eValue = emotion.GetEmotValue(content);
                        obj.put("emotValue", eValue);
                        obj.put("emotPolarity", emotion.GetEmotPolarity(eValue));

                        String msg = obj.toString();

                        producer.produce(StreamProducer.ROUTE_STREAM + obj.getString("roomID"), msg);
                        System.out.println(String.format("%4.2f %s", emotion.GetEmotValue(content), content));
                    }
                }
            };

            channel.basicConsume(QUEUE_NAME, true, consumer);
        }
    }


    public static void main(String[] argv) throws IOException, TimeoutException {
        EmotConsumer parser = new EmotConsumer();
        parser.consume(new StreamProducer());
    }
}
