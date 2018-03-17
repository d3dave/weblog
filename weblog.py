import logging
import logging.handlers
import http.server
import socketserver
import time
import json
import threading
import random
import string
import queue
import webbrowser

import websocket


class Handler(http.server.SimpleHTTPRequestHandler):
    log_queue = queue.Queue()

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.ws = None

    def do_GET(self):
        try:
            ws = websocket.WebSocket()
            ws.accept(self.request, self.headers)
            self.ws = ws
            self.log_request(101)
            return self.ws_handler()
        except websocket.WebSocketError:
            pass

        super().do_GET()

    def ws_handler(self):
        while True:
            record = self.log_queue.get()
            result = {
                'time': record.asctime,
                'name': record.name,
                'level': record.levelname,
                'msg': record.getMessage(),
                'thread': record.threadName,
            }
            try:
                self.ws.send(json.dumps(result))
            except ConnectionAbortedError:
                return


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass


def log_stuff():
    levels = [
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL
    ]
    gen_word = lambda n: random.choice(string.ascii_letters) + ''.join(random.choice(string.ascii_lowercase) for _ in range(n))
    gen_phrase = lambda n: ' '.join(gen_word(random.randint(3, 9)) for _ in range(n))
    logging.log(random.choice(levels), gen_phrase(random.randint(5, 20)))


def main():
    server = ThreadedHTTPServer(('', 80), Handler)
    threading.Thread(target=server.serve_forever).start()
    webbrowser.open('http://localhost')

    handler = logging.handlers.QueueHandler(Handler.log_queue)
    handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(name)s %(levelname)s %(message)s %(threadName)s'))
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)

    while True:
        log_stuff()
        log_stuff()
        time.sleep(2)


if __name__ == '__main__':
    main()
