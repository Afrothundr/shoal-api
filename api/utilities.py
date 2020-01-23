import requests
import os
import environ

class Utilities:
    def api_request(self, path):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_file = os.path.join(BASE_DIR, '.env')

        env = environ.Env()
        # reading .env file
        environ.Env.read_env(env_file)
        url = env('API_BASE_URL') + path
        headers = {
            'X-ListenAPI-Key': env('API_KEY'),
        }
        return requests.request('GET', url, headers=headers)