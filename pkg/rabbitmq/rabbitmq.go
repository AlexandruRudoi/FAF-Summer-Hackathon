package rabbitmq

import (
	"github.com/streadway/amqp"
)

func ConnectToRabbitMQ() *amqp.Channel {
	// Establish a connection to RabbitMQ server
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	if err != nil {
		return nil
	}

	ch, err := conn.Channel()
	if err != nil {
		return nil
	}

	return ch
}
