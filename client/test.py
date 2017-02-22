import multiprocessing
import client_ui
try:
    def attack():
    	print 'Client Opened'
        client_ui.start_client()
    for i in range(3):
        z = multiprocessing.Process(target=attack)
        z.start()
        process.append(z)
except KeyboardInterrupt:
    for a in process:
        a.terminate()