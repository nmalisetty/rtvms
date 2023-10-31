from app import alerts_consumer
from dotenv import load_dotenv
import threading

if __name__ == '__main__':
    load_dotenv()
    print('Starting alerts kafka consumer thread')

    alerts_thread = threading.Thread(target=alerts_consumer)
    alerts_thread.start()
