from math import fabs


class ProcessPorts:
    def __init__(self, data):
        self.port_data = data
        self.port_lon_lat = self.convert()

    def convert(self):
        port_lat_lon = []
        for port in self.port_data:
            name = port.get('Name', '')
            x = int(port['Position']['x'] / 100)
            z = int(port['Position']['z'] / 100)

            carl_x, carl_z = -234.0, -120.0
            wilm_x, wilm_z = -116.0, -7906.0
            delta_x = fabs(carl_x - wilm_x)
            delta_z = fabs(carl_z - wilm_z)
            delta_x_grad = fabs(75.54 - 75.77)
            delta_z_grad = fabs(20.23 - 35.44)

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
