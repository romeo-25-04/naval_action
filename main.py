import pprint
from NA_data.get_data import GetData
from NA_data.process_data import ProcessData
from NA_data.process_ports import ProcessPorts

pp = pprint.PrettyPrinter(indent=2)


def main():
    na_data = GetData('PvEeu')
    item_data = na_data.item_data
    ports_data = na_data.ports_data
    processed_data = ProcessData(item_data)
    processed_ports = ProcessPorts(ports_data)

    for item_id in [348,349,350,351,352]:
        item = processed_data.get_item_by_id(item_id)
        pp.pprint({
            'Name': item.get('Name', None),
            'Id': item.get('Id', None),
            'scoreValue': item.get('scoreValue', None),
            'Modifiers': item.get('Modifiers', None)
        })

    # pp.pprint(processed_ports.port_data[0])
    # pp.pprint(len(processed_data.modules))
    # locean_ship = [ship
    #                for ship in processed_data.ships
    #                if ship.get('Name', None) == "L'Ocean"
    #                ][0]
    # pp.pprint(locean_ship)

    # ship_id = 650
    # print([ship_id])
    # pp.pprint(processed_data.get_ships_recipe(ship_id))

    # print(len(processed_data.wood_types))
    # pp.pprint(processed_data.wood_types)

    # pp.pprint(processed_data.ships_bp[0])
    # pp.pprint(processed_data.materials)
    # sort_to_lab = sorted(ships_bp, key=lambda k: k['LaborPrice'], reverse=True)
    bla = ""

    # reg_bonuses = processed_data.reg_bonuses
    # print(len(reg_bonuses))
    # print(navigate())

if __name__ == "__main__":
    main()
