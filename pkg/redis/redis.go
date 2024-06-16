package redis

import (
	"context"
	"log"

	"github.com/redis/go-redis/v9"
)

func NewRedisConnection() *redis.Client {
	client := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "redis",
		DB:       0,
	})

	// Ping the redis server to check if it is alive
	ctx := context.Background()
	pong, err := client.Ping(ctx).Result()
	if err != nil {
		log.Fatalf("failed to connect to redis: %v\n", err)
	}

	log.Printf("connected to redis: %v\n", pong)
	return client
}
