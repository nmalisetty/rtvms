from app import alerts_consumer
import threading

if __name__ == '__main__':
    print('Starting alerts kafka consumer thread')
    alerts_thread = threading.Thread(target=alerts_consumer)
    alerts_thread.start()
