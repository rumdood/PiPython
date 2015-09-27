from azure.servicebus import ServiceBusService, Message, Queue

class azure_service_bus_listener(object):
	
	def __init__(self, azure_settings):
		self.bus_service = ServiceBusService(
			service_namespace= azure_settings.name_space,
			shared_access_key_name = azure_settings.key_name,
			shared_access_key_value = azure_settings.key_value)
		
		self.queue_name = azure_settings(queue_name)
	
	def wait_for_message(self, on_receive_target):
		message = self.bus_service.receive_queue_message(self.queue_name, peek_lock=False)
		message_string = message.body.decode('utf-8')
		on_receive_target(message_string)
		
	def create_queue(self):
		q_opt = Queue()
		q_opt.max_size_in_megabytes = '1024'
		q_opt.default_message_time_to_live = 'PT1M'
		self.bus_service.create_queue(self.queue_name, q_opt)