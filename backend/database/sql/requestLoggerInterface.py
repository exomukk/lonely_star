import json
from database.sql.dbInterface import DatabaseInterface
from Geocoder.geocoderInterface import geocoderInterface
class requestLoggerInterface:
    def __init__(self):
        self.databaseInterface = DatabaseInterface()
        self.geocoderInterface = geocoderInterface()

    def check_abnormal_request(self, ip, user_id, request_url):
        if self.databaseInterface.check_abnormal_request(ip, user_id, request_url):
            geo_location = self.geocoderInterface.get_location_from_ip(ip)
            geo_location_str = json.dumps(geo_location)
            city = self.geocoderInterface.get_city_from_ip(ip)
            self.add_request_log(ip, user_id, request_url,geo_location_str, city)
            return False
        else:
            return True

    def add_request_log(self, user_id,request_url,ip_address,geo_location,city):
        self.databaseInterface.add_request_log(user_id,request_url,ip_address,geo_location,city)
        pass