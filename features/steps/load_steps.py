######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Product Steps

Steps file for products.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
from behave import given
import requests
from service import status

@given('the following products exist:')
def step_impl(context):
    # clear out any existing
    requests.delete(context.base_url + "/products")
    # load each row
    for row in context.table:
        payload = {
            "name":        row['name'],
            "description": row['description'],
            "price":       float(row['price']),
            "available":   row['available'].lower() in ("true","1"),
            "category":    row['category']
        }
        resp = requests.post(context.base_url + "/products", json=payload)
        assert resp.status_code == status.HTTP_201_CREATED
