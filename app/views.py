from flask import render_template, request
from app import app

from NA_data.get_data import GetData
from NA_data.process_data import ProcessData
from NA_data.process_ports import ProcessPorts
from math import atan, degrees, radians, fabs, acos, sin, cos

na_data = GetData('PvEeu')
item_data = na_data.item_data
processed_data = ProcessData(item_data)
materials = processed_data.materials
resources = processed_data.resources
mat_res = materials + resources
reg_bonuses = processed_data.reg_bonuses
mods = processed_data.modules

processed_ports = ProcessPorts(na_data.ports_data)
ports = processed_ports.port_lon_lat


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="General")


@app.route('/crafting')
@app.route('/crafting/<int:ship_id>/<int:quality>/<int:wood_nr>')
def crafting_id(ship_id=650, quality=0, wood_nr=0):
    ship = processed_data.get_item_by_id(ship_id)
    print([ship])
    recipe = processed_data.get_ships_recipe(ship.get('Id', None))
    ship_list = [{'Name': item.get('Name', None),
                  'Id': item.get('Id', None)}
                 for item in sorted(processed_data.ships, key=lambda k: k['SortingGroup'])]
    page = render_template('crafting.html',
                           title='Crafting',
                           ship_id=ship_id,
                           quality=quality,
                           wood_nr=wood_nr,
                           ships=ship_list,
                           ship=ship,
                           recipe=recipe,
                           mat_res=mat_res,
                           wood_modif=processed_data.wood_types)
    return page


@app.route('/regional_bonuses')
def regional_bonuses():
    return render_template('bonuses.html',
                           title='Regional Bonuses',
                           reg_bonuses=reg_bonuses)


@app.route('/modules')
def modules():
    modules_by_name = {}
    for mod in mods:
        if modules_by_name.get(mod['Name'], []):
            modules_by_name[mod['Name']].append(mod)
        else:
            modules_by_name[mod['Name']] = [mod]
    mod_keys = list(modules_by_name.keys())
    print(mod_keys)
    return render_template('modules.html',
                           title='Modules',
                           mod_keys=mod_keys,
                           mods=modules_by_name)


def direction(my_pos, port):
    x = my_pos['x']
    y = my_pos['y']
    a = port['a']
    b = port['b']
    alfa = 0
    if b != y:
        if x >= a and b > y:
            alfa = degrees(atan((x-a)/(b-y)))
        elif x > a and b < y:
            alfa = degrees(atan((y - b) / (x - a))) + 90
        elif x <= a and b < y:
            alfa = degrees(atan((a - x) / (y - b))) + 180
        elif x < a and b > y:
            alfa = degrees(atan((b - y) / (a - x))) + 270
    elif a < x:
        alfa = 90
    elif a > x:
        alfa = 270
    return round(alfa, 0)


def distance(my_pos, port_pos):
    fi1 = radians(port_pos['b'])
    fi2 = radians(my_pos['x'])
    delta = radians(port_pos['a'] - my_pos['x'])
    earth_R = 6371000
    dist_m = acos(sin(fi1) * sin(fi2) + cos(fi1) * cos(fi2) * cos(delta)) * earth_R
    dist_km = dist_m / 1000
    return round(dist_km, 0)


@app.route('/navigate', methods=['GET', 'POST'])
def navigate():
    destination = {'a': 0.0, 'b': 0.0}
    my_pos = {'x': 0.0, 'y': 0.0}
    angle = 0
    dist = 0
    if request.method == 'POST':
        destination['a'] = float(request.form['dest_a'])
        destination['b'] = float(request.form['dest_b'])
        my_pos['x'] = float(request.form['my_pos_x'])
        my_pos['y'] = float(request.form['my_pos_y'])
        angle = direction(my_pos=my_pos, port=destination)
        dist = distance(my_pos, port_pos=destination)
    return render_template('navigate.html',
                           title='Navigation',
                           destination=destination,
                           my_pos=my_pos,
                           angle=-angle,
                           ports=ports,
                           dist=dist)

@app.route('/compare')
def compare():
    return render_template('compare.html',
                           title='Compare Ships')
