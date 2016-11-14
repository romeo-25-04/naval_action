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

            carl_x, carl_z = -23400.0005230308, -12000.0002682209
            pr_x, pr_z = -42400.0009477139, -22600.0005051494
            delta_x = carl_x - pr_x
            delta_z = carl_z - pr_z
            delta_x_grad = 75.56 - 75.18
            delta_z_grad = 20.22 - 20.75

            one_grad_x = delta_x/delta_x_grad
            one_grad_z = delta_z / delta_z_grad

            x_grad = x/one_grad_x
            z_grad = z/one_grad_z
            lon = 76.00 + x_grad
            lat = 20.00 - z_grad
            port_lat_lon.append({
                'Name': name,
                'lon': round(lon, 2),
                'lat': round(lat, 2)
            })
        return port_lat_lon
