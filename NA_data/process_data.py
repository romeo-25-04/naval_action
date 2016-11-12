class ProcessData:
    def __init__(self, data):
        self.data = data
        self.ships = self.get_ships()
        self.ships_bp = self.get_items_by_type('RecipeShip')
        self.resources = self.get_items_by_type('Resource')
        self.materials = self.get_items_by_type('Material')
        self.modules = self.get_items_by_type('Module')
        self.wood_types = self.get_wood_types()
        self.reg_bonuses = self.get_reg_bonuses()

    def get_item_by_id(self, item_id):
        for item in self.data:
            if int(item.get('Id', 0)) == item_id:
                return item
        return None

    def get_item_by_name(self, name):
        for item in self.data:
            if item.get('Name', None) == name:
                return item

    def get_items_by_type(self, item_type):
        items = []
        for item in self.data:
            if item.get('ItemType', None) == item_type:
                items.append(item)
        return items

    def get_ships_recipe(self, ship_id):
        for recipe in self.ships_bp:
            if recipe.get('Results', None)[0].get('Template', None) == ship_id:
                return recipe
        return None

    def get_wood_types(self):
        return {i: item.get('Modifiers', None)
                for i, wood in enumerate(['Fir', 'Oak', 'Teak', 'Live Oak', 'Mahogany', 'Bermuda Cedar'])
                for item in self.data
                if item.get('Name', None) == wood + ' Wood Type'}

    def get_reg_bonuses(self):
        return [item for item in self.data
                if item.get('Name', None).lower().endswith('bonus')]

    def get_ships(self):
        ships = []
        for ship in self.get_items_by_type('Ship'):
            ship_speed = ship.get('Specs', None).get('MaxSpeed', None)
            ship_speed = round(float(ship_speed) / 10, 2)
            ship_speed = '{:.2f}'.format(ship_speed)
            ship['Specs']['MaxSpeed'] = ship_speed
            ships.append(ship)
        return ships
