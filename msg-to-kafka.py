def run(self) -> NoReturn:
        """Continuously fetch and send messages to a Kafka topic."""
        while self.running.is_set():
            try:
                messages: List[CommonDocument] = self.fetch_function()
                if messages:
                    messages = [msg.to_kafka_payload() for msg in messages]
                    self.producer.send(self.topic, value=messages)
                    self.producer.flush()
                logger.info(
                    f"Producer : {self.producer_id} sent: {len(messages)} msgs."
                )
                time.sleep(self.wait_window_sec)
            except Exception as e:
                logger.error(f"Error in producer worker {self.producer_id}: {e}")
                self.running.clear()  # Stop the thread on error