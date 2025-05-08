import geocoder
class geocoderInterface:
    def __init__(self):
        self.geocoder=geocoder

    def get_location_from_ip(self,ip):
        g = self.geocoder.ip(ip)
        if g.ok:
            return g.latlng
        else:
            return None

    def get_city_from_ip(self,ip):
        g = self.geocoder.ip(ip)
        if g.ok:
            return g.city
        else:
            return None