# outputs.tf
output "sqs_queue_url" {
  value = aws_sqs_queue.follow_event_queue.id
}
