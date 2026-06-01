# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_space import Facilities
from myuw.models import CampusBuilding
from myuw.test.api import MyuwApiTest


class TestBuilding(MyuwApiTest):
    def test_building(self):
        location_url = "https://map.uw.edu/?id=2099#!m/974994?share"
        fac_obj = Facilities().search_by_number("1347")
        b_obj = CampusBuilding.upd_building(fac_obj)
        b_obj.location_url = location_url
        b_obj.save()
        self.assertEqual(b_obj.latitude, 47.6536929997)
        self.assertEqual(b_obj.longitude, -122.304747)
        self.assertEqual(b_obj.name, "Mechanical Engineering Building")
        self.assertEqual(b_obj.code, 'MEB')
        self.assertEqual(b_obj.number, '1347')
        self.assertEqual(b_obj.location_url, location_url)
        self.assertEqual(
            b_obj.json_data(),
            {
                'code': 'MEB',
                'latitude': 47.6536929997,
                'longitude': -122.304747,
                'name': 'Mechanical Engineering Building',
                'number': '1347',
                'location_url': location_url,
            }
        )
        self.assertIsNotNone(str(b_obj))

        obj1 = CampusBuilding.get_building_by_code('MEB')
        self.assertEqual(
            obj1.json_data(),
            {
                'code': 'MEB',
                'latitude': '47.6536929997',
                'longitude': '-122.304747',
                'name': 'Mechanical Engineering Building',
                'number': '1347',
                'location_url': location_url,
            }
        )

        obj2 = CampusBuilding.get_building_by_number('1347')
        obj2.location_url = obj2._google_map_url()
        self.assertEqual(
            obj2.json_data(),
            {
                'code': 'MEB',
                'latitude': '47.6536929997',
                'longitude': '-122.304747',
                'name': 'Mechanical Engineering Building',
                'number': '1347',
                'location_url': (
                    'https://maps.google.com/maps?q=47.6536929997,'
                    '-122.304747+(MEB)&t=k&z=18'),
            }
        )

        self.assertTrue(CampusBuilding.exists('MEB'))
        self.assertTrue(CampusBuilding.exists_by_number('1347'))

        fac_obj.code = 'MEBB'
        obj3 = CampusBuilding.upd_building(fac_obj)
        self.assertEqual(obj3.code, 'MEBB')
        self.assertFalse(b_obj == obj3)
