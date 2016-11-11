class ProcessPorts:
    def __init__(self, data):
        self.port_data = data
        self.port_lon_lat = self.convert()

    def convert(self):
        port_lat_lon = []
        for port in self.port_data:
            name = port.get('Name', '')
            x = port['Position']['x']
            z = port['Position']['z']

            carl_x, carl_z = -23400.0005230308, 0
            pr_x, pr_z = -42400.0009477139, 0
            delta_x = carl_x - pr_x
            delta_x_grad = 75.56 - 75.18
            one_grad = delta_x/delta_x_grad

            x_grad = x/one_grad
            z_grad = z/one_grad
            lon = 76.00 + x_grad
            lat = 20.00 - z_grad
            port_lat_lon.append({
                'Name': name,
                'lon': round(lon, 2),
                'lat': round(lat, 2)
            })
        return port_lat_lon
