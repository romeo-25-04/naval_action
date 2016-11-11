import requests
import json
import os


class GetData:
    MAIN_URL = 'https://storage.googleapis.com/nacleanopenworldprodshards/'
    ITEM_TEMPLATE = 'ItemTemplates_{}.json'
    SHOPS_TEMPLATE = 'Shops_{}.json'
    PORTS_TEMPLATE = 'Ports_{}.json'
    NATIONS_TEMPLATE = 'Nations_{}.json'
    SERVERS = {
        'PvPeu':'cleanopenworldprodeu1',
        'PvEeu':'cleanopenworldprodeu2',
        'PvPus':'cleanopenworldprodus2'
    }
    LOCAL_DATA_PATH = 'local_data'

    def __init__(self, server):
        self.server_template = self.SERVERS.get(server, None)
        self.item_data = None
        self.shop_data = None
        self.ports_data = None
        self.nations_data = None
        if self.empty_local() and self.server_template:
            self.item_data = self.call_api(self.ITEM_TEMPLATE)
            self.shop_data = self.call_api(self.SHOPS_TEMPLATE)
            self.ports_data = self.call_api(self.PORTS_TEMPLATE)
            self.nations_data = self.call_api(self.NATIONS_TEMPLATE)
        else:
            self.item_data = self.json_from_file(
                self.LOCAL_DATA_PATH + '/' +
                self.ITEM_TEMPLATE.format(self.server_template)
            )
            self.shop_data = self.json_from_file(
                self.LOCAL_DATA_PATH + '/' +
                self.SHOPS_TEMPLATE.format(self.server_template)
            )
            self.ports_data = self.json_from_file(
                self.LOCAL_DATA_PATH + '/' +
                self.PORTS_TEMPLATE.format(self.server_template)
            )
            self.nations_data = self.json_from_file(
                self.LOCAL_DATA_PATH + '/' +
                self.NATIONS_TEMPLATE.format(self.server_template)
            )

    def empty_local(self):
        return not os.listdir(self.LOCAL_DATA_PATH)

    def call_api(self, template):
        json_name = template.format(self.server_template)
        call_url = self.MAIN_URL + json_name
        print('calling:', call_url)
        try:
            msg = requests.get(call_url)
            print(msg.status_code)
            print(msg.encoding)
            msg.encoding = 'utf-8'
            list1 = msg.text.split('=')
            str_data = list1[1].strip()[:-1]
            file_handler = open(self.LOCAL_DATA_PATH + '/' + json_name, "w")
            file_handler.write(str_data)
            file_handler.close()
            return json.loads(str_data)
        except Exception as err:
            print('Something went wrong:', err)
            return {}

    def json_from_file(self, path):
        print("load from file:", path)
        with open(path) as fileHandler:
            return json.load(fileHandler)
