# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_space import Facilities
from myuw.models.campus_building import Buildings
from myuw.test.api import MyuwApiTest


class TestBuilding(MyuwApiTest):
    def test_building(self):
        fac_obj = Facilities().search_by_number("1347")
        b_obj = Buildings.upd_building(fac_obj)
        self.assertEquals(b_obj.latitude, '47.653693')
        self.assertEquals(b_obj.longitude, '-122.304747')
        self.assertEquals(b_obj.name, "Mechanical Engineering Buildin")
        self.assertEquals(b_obj.code, 'MEB')
        self.assertEquals(b_obj.number, '1347')
        self.assertEquals(
            b_obj.json_data(),
            {
                'code': 'MEB',
                'latitude': '47.653693',
                'longitude': '-122.304747',
                'name': 'Mechanical Engineering Building',
                'number': '1347',
            }
        )
        self.assertIsNotNone(str(b_obj))

        obj1 = Buildings.get_building_by_code('MEB')
        self.assertEquals(b_obj, obj1)

        obj2 = Buildings.get_building_by_number('1347')
        self.assertEquals(b_obj, obj2)

        self.assertTrue(Buildings.exists('MEB'))
        self.assertTrue(Buildings.exists_by_number('1347'))

        fac_obj.code = 'MEBB'
        obj3 = Buildings.upd_building(fac_obj)
        self.assertEquals(obj3.code, 'MEBB')
        self.assertFalse(b_obj == obj3)

        fac_obj.number = '1348'
        obj4 = Buildings.upd_building(fac_obj)
        self.assertEquals(obj4.number, '1348')
        self.assertFalse(b_obj == obj4)
