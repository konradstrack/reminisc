import queue

# main queue which should be filled by modules and emptied by the command processor
command_queue = queue.Queue(maxsize=1000)