# Name          :     Mattrey Kumar Rana
# Email         :     mrana23@myseneca.ca
# Student ID    :     116092222

import http
import unittest
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
import http.client
import json
import threading

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8000)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_get_method(self):
        
        connection = http.client.HTTPConnection(*self.server_address)
        connection.request('GET', '/')
        response = connection.getresponse()

        
        data = response.read().decode()
        connection.close()

      
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

      
        response_data = json.loads(data)
        self.assertEqual(response_data, {'message': 'This is a GET request response'})

    def test_post_method(self):
       
        connection = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-type': 'application/json'}
        test_data = {'key': 'value'}
        connection.request('POST', '/', body=json.dumps(test_data), headers=headers)
        response = connection.getresponse()

     
        data = response.read().decode()
        connection.close()

        self.assertEqual(response.status, 200)
        self.assertEqual(response.getheader('Content-Type'), 'application/json')
        response_data = json.loads(data)
        self.assertEqual(response_data, {'received': test_data})

if __name__ == '__main__':
    unittest.main()