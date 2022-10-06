import configparser
config = configparser.RawConfigParser()
config.read(filenames="../config.properties")

google_api_key = config.get("google.com", "api-key")
secret_key = config.get("mrbond.com", "secret")
sheety_api = config.get("mrbond.com", "sheety-api")
sheety_token = config.get("mrbond.com", "sheety-token")