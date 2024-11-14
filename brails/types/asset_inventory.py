# Copyright (c) 2024 The Regents of the University of California
#
# This file is part of BRAILS++.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# You should have received a copy of the BSD 3-Clause License along with
# BRAILS. If not, see <http://www.opensource.org/licenses/>.
#
# Contributors:
# Barbaros Cetiner
# Frank McKenna
#
# Last updated:
# 11-06-2024

"""
This module defines classes associated with asset inventories.

.. autosummary::

    AssetInventory
    Asset
"""

import random
import json
from datetime import datetime
from importlib.metadata import version
from typing import Any
import csv
import logging
import numpy as np
import pandas as pd
from brails.utils import InputValidator

# Configure logging:
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Asset:
    """
    A data structure for an asset that holds it coordinates and features.

    Attributes:
        asset_id (str|int):: Unique identifier for the asset.
        coordinates (list[List[float]]): A list of coordinate pairs
            [[lon1, lat1], [lon2, lat2], ..., [lonN, latN]].
        features (dict[str, any]): A dictionary of features (attributes) for
            the asset.

    Methods:
        add_features(additional_features: dict[str, any],
            overwrite: bool = True): Update the existing features in the asset.
        print_info(): Print the coordinates and features of the asset.
    """

    def __init__(self,
                 asset_id: str | int,
                 coordinates: list[list[float]],
                 features: dict[str, Any] = None):
        """
        Initialize an Asset with an asset ID, coordinates, and features.

        Args:
            asset_id (str|int): The unique identifier for the asset.
            coordinates (list[list[float]]): A two-dimensional list
                representing the geometry of the asset in [[lon1, lat1],
                [lon2, lat2], ..., [lonN, latN]] format.
            features (dict[str, Any], optional): A dictionary of features.
                Defaults to an empty dict.
        """
        coords_check, output_msg = InputValidator.validate_coordinates(
            coordinates)
        if coords_check:
            self.coordinates = coordinates
        else:
            logger.warning('%s Setting coordinates for asset %s to an empty '
                           'list.', output_msg, asset_id)
            self.coordinates = []

        self.features = features if features is not None else {}

    def add_features(self, additional_features: dict, overwrite: bool = True):
        """
        Update the existing features in the asset.

        Args:
            additional_features (dict[str, any]): New features to merge into
                the asset's features.
            overwrite (bool, optional): Whether to overwrite existing features.
                Defaults to True.
        """
        if overwrite:
            # Overwrite existing features with new ones:
            self.features.update(additional_features)
        else:
            # Only update with new keys, do not overwrite existing keys:
            for key, value in additional_features.items():
                if key not in self.features:
                    self.features[key] = value

    def print_info(self):
        """Print the coordinates and features of the asset."""
        print('\t Coordinates: ', self.coordinates)
        print('\t Features: ', self.features)


class AssetInventory:
    """
    A class representing a Asset Inventory.

    Attributes:
        inventory (dict): The inventory stored in a dict accessed by asset_id

     Methods:
        print_info(): Print the asset inventory.
        add_asset(asset_id, Asset): Add an asset to the inventory.
        add_asset_coordinates(asset_id, coordinates): Add an asset to the
            inventory with just a list of coordinates.
        add_asset_features(asset_id, features): Append new features to the
            asset.
        remove_asset(asset_id): Remove an asset to the inventory.
        get_asset_features(asset_id): Get coordinates of a particular assset.
        get_asset_coordinates(asset_id): Get features of a particular assset.
        get_asset_ids(): Return the asset ids as a list.
        get_random_sample(size, seed): Get subset of the inventory.
        get_coordinates(): Return a list of footprints.
        get_geojson(): Return inventory as a geojson dict.
        write_to_geojson(): Wtite inventory to file in GeoJSON format. Also return inventory as a geojson dict!
        read_from_csv(file_path, keep_existing, str_type, id_column): Read
            inventory dataset from a csv table
        add_asset_features_from_csv(file_path, id_column): Add asset features
            from a csv file.
    """

    def __init__(self):
        """Initialize AssetInventory with an empty inventory dictionary."""
        self.inventory = {}

    def print_info(self):
        """Print the asset inventory."""
        print(self.__class__.__name__)
        print("Inventory stored in: ", self.inventory.__class__.__name__)
        for key, asset in self.inventory.items():
            print("Key: ", key, "Asset:")
            asset.print_info()

    def add_asset(self, asset_id: str | int, asset: Asset) -> bool:
        """
        Add an Asset to the inventory.

        Args:
            asset_id (str|int): The unique identifier for the asset.
            asset (Asset): The asset to be added.

        Returns:
            bool: True if the asset was added successfully, False otherwise.
        """
        existing_asset = self.inventory.get(asset_id, None)

        if existing_asset is not None:
            logger.warning('Asset with id %s already exists. Asset was not '
                           'added', asset_id)
            return False

        self.inventory[asset_id] = asset

        return True

    def add_asset_coordinates(self,
                              asset_id: str | int,
                              coordinates: list[list[float]]) -> bool:
        """
        Add an Asset to the inventory by adding its coordinate information.

        Args:
            asset_id (str|int): The unique identifier for the asset.
            coordinates (list[list[float]]): A two-dimensional list
                representing the geometry in [[lon1, lat1], [lon2, lat2], ...,
                [lonN, latN]] format.

        Returns:
            bool: True if the asset was added successfully, False otherwise.
        """
        existing_asset = self.inventory.get(asset_id, None)

        if existing_asset is not None:
            logger.warning('Asset with id %s already exists. Coordinates were '
                           'not added', asset_id)
            return False

        # Create asset and add using id as the key:
        asset = Asset(asset_id, coordinates)
        self.inventory[asset_id] = asset

        return True

    def add_asset_features(self,
                           asset_id: str | int,
                           new_features: dict,
                           overwrite=True) -> bool:
        """
        Add new asset features to the Asset with the specified ID.

        Args:
            asset_id (str|int): The unique identifier for the asset.
            new_features (dict): A dictionary of features to add to the asset.
            overwrite (bool): Whether to overwrite existing features with the
                same keys. Defaults to True.

        Returns:
            bool: True if features were successfully added, False if the asset
                does not exist or the operation fails.
        """
        asset = self.inventory.get(asset_id, None)
        if asset is None:
            logger.warning('No existing Asset with id % s found. Asset '
                           'features not added.', asset_id)
            return False

        return asset.add_features(new_features, overwrite)

    def remove_asset(self, asset_id: str | int) -> bool:
        """
        Remove an Asset from the inventory.

        Args:
            asset_id (str|int): The unique identifier for the asset.

        Returns:
            bool: True if asset was removed, False otherwise.
        """
        del self.inventory[asset_id]

        return True

    def get_asset_features(self, asset_id: str | int) -> tuple[bool, dict]:
        """
        Get features of a particular asset.

        Args:
            asset_id (str|int): The unique identifier for the asset.

        Returns:
            tuple[bool, Dict]: A tuple where the first element is a boolean
                indicating whether the asset was found, and the second element
                is a dictionary containing the asset's features if the asset
                is present. Returns an empty dictionary if the asset is not
                found.
        """
        asset = self.inventory.get(asset_id, None)
        if asset is None:
            return False, {}

        return True, asset.features

    def get_asset_coordinates(self, asset_id: str | int) -> tuple[bool, list]:
        """
        Get the coordinates of a particular asset.

        Args:
            asset_id (str | int): The unique identifier for the asset.

        Returns:
            tuple[bool, list]]: A tuple where the first element is a boolean
                indicating whether the asset was found, and the second element
                is a list of coordinate pairs in the format [[lon1, lat1],
                [lon2, lat2], ..., [lonN, latN]] if the asset is present.
                Returns an empty list if the asset is not found.
        """
        asset = self.inventory.get(asset_id, None)
        if asset is None:
            return False, []

        return True, asset.coordinates

    def get_asset_ids(self) -> list[str | int]:
        """
        Retrieve the IDs of all assets in the inventory.

        Returns:
            list[str | int]: A list of asset IDs, which may be strings or
                integers.
        """
        return list(self.inventory.keys())

    def get_random_sample(self,
                          nsamples: int,
                          seed: int | float | str | bytes | bytearray = None):
        """
        Generate a smaller AssetInventory with a random selection of assets.

        Args:
            nsamples (int): The number of assets to include in the sampled
                inventory.
            seed (int | float | str | bytes | bytearray | None): The seed for
                the random generator. If None, the seed is set to the sytem
                default (i.e., the current system time).

        Returns:
           AssetInventory: A new AssetInventory instance containing a random
               subset of assets.
        """
        result = AssetInventory()
        if seed is not None:
            random.seed(seed)

        random_keys = random.sample(list(self.inventory.keys()), nsamples)
        for key in random_keys:
            result.add_asset(key, self.inventory[key])

        return result

    def get_coordinates(self) -> tuple[list[list[list[float, float]]],
                                       list[str | int]]:
        """
        Get geometry (coordinates) and keys of all assets in the inventory.

        Returns:
            tuple[list[list[list[float, float]]], list[str | int]]: A tuple
                containing:
                - A list of coordinates for each asset, where each coordinate
                    is represented as a list of [longitude, latitude] pairs.
                - A list of asset keys corresponding to each Asset.
        """
        result_coordinates = []
        result_keys = []
        for key, asset in self.inventory.items():
            result_coordinates.append(asset.coordinates)
            result_keys.append(key)

        return result_coordinates, result_keys

    def get_geojson(self) -> dict:
        """
        Generate a GeoJSON representation of the assets in the inventory.

        Returns:
            dict: A dictionary in GeoJSON format containing all assets, with
                each asset represented as a feature. Each feature includes the
                geometry (Point or Polygon) and associated properties.
        """
        geojson = {'type': 'FeatureCollection',
                   'generated': str(datetime.now()),
                   'brails_version': version('BRAILS'),
                   'crs': {'type': 'name',
                           'properties': {
                               'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}
                           },
                   'features': []
                   }

        for key, asset in self.inventory.items():
            if len(asset.coordinates) == 1:
                geometry = {"type": "Point",
                            "coordinates": [asset.coordinates[0][:]]
                            }
            elif len(asset.coordinates) == 2:
                geometry = {"type": "Line",
                            "coordinates": sset.coordinates
                            }                
            else:
                geometry = {'type': 'Polygon',
                            'coordinates': [asset.coordinates]
                            }

            feature = {'type': 'Feature',
                       'properties': asset.features,
                       'geometry': geometry
                       }
            
            # fmk - Feature is what is needed in geojson
            #if 'type' in asset.features:
            #    feature['type'] = asset.features['type']

            geojson['features'].append(feature)
            # TODO: Note from SY here we could put in NA! for imputation and
            # ensure all features have same set of keys!!

        return geojson

    def write_to_geojson(self, output_file: str = '') -> dict:
        """
        Generate a GeoJSON representation of the assets in the inventory.

        Returns:
            dict: A dictionary in GeoJSON format containing all assets, with
                each asset represented as a feature. Each feature includes the
                geometry (Point or Polygon) and associated properties.
        """
        geojson = {'type': 'FeatureCollection',
                   'generated': str(datetime.now()),
                   'brails_version': version('BRAILS'),
                   'crs': {'type': 'name',
                           'properties': {
                               'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}
                           },
                   'features': []
                   }

        for key, asset in self.inventory.items():
            if len(asset.coordinates) == 1:
                geometry = {"type": "Point",
                            "coordinates": [asset.coordinates[0][:]]
                            }
            elif len(asset.coordinates) == 2:
                geometry = {"type": "Point",
                            "coordinates": asset.coordinates
                            }                
            else:
                geometry = {'type': 'Polygon',
                            'coordinates': [asset.coordinates]
                            }

            feature = {'type': 'Feature',
                       'properties': asset.features,
                       'geometry': geometry
                       }
            
            # fmk - NOPE - not geojson
            #if 'type' in asset.features:
            #    feature['type'] = asset.features['type']

            geojson['features'].append(feature)
            # TODO: Note from SY here we could put in NA! for imputation and
            # ensure all features have same set of keys!!

        # Write the created GeoJSON dictionary into a GeoJSON file:
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as file_out:
                json.dump(geojson, file_out, indent=2)

        return geojson

    def read_from_csv(self, file_path, keep_existing, str_type="building", id_column=None) -> bool:
        """
        Read inventory data from a CSV file and add it to the inventory.

        Args:
            file_path (str):
                  The path to the CSV file
            keep_existing (bool):
                  If False, the inventory will be initialized
            str_type (str):
                  "building" or "bridge"
            id_column (str):
                  The name of column that contains id values. If None, new indicies will be assigned

        Returns:
            bool:
                  True if assets were addded, False otherwise.
        """

        def is_float(element: any) -> bool:
            # If you expect None to be passed:
            if element is None:
                return False
            try:
                float(element)
                return True
            except ValueError:
                return False
            pass

        if keep_existing:
            if len(self.inventory) == 0:
                print("No existing inventory found. Creating a new inventory")
                id_counter = 1
            else:
                # we don't want a duplicate the id
                id_counter = max(self.inventory.keys()) + 1
        else:
            self.inventory = {}
            id_counter = 1

        # Attempt to open the file
        try:
            with open(file_path, mode="r") as csvfile:
                csv_reader = csv.DictReader(csvfile)
                rows = list(csv_reader)
        except FileNotFoundError:
            raise Exception("The file {} does not exist.".format(csvfile))

        # Check if latitude/longitude exist
        lat = ['latitude', 'lat']
        lon = ['longitude', 'lon']
        key_names = csv_reader.fieldnames
        lat_id = np.where([y.lower() in lat for y in key_names])[0]
        lon_id = np.where([x.lower() in lon for x in key_names])[0]
        if len(lat_id) == 0:
            raise Exception(
                "The key 'Latitude' or 'Lat' (case insensitive) not found. Please specify the building coordinate.")
        if len(lon_id) == 0:
            raise Exception(
                "The key 'Longitude' or 'Lon' (case insensitive) not found. Please specify the building coordinate.")
        lat_key = key_names[lat_id[0]]
        lon_key = key_names[lon_id[0]]

        for bldg_features in rows:
            for i, key in enumerate(bldg_features):

                # converting to a number
                val = bldg_features[key]
                if val.isdigit():
                    bldg_features[key] = int(val)
                elif is_float(val):
                    bldg_features[key] = float(val)

            # coordinates = [[bldg_features[lat_key], bldg_features[lon_key]]]
            coordinates = [[bldg_features[lon_key], bldg_features[lat_key]]]

            bldg_features.pop(lat_key)
            bldg_features.pop(lon_key)

            # TODO: what should the types be?
            if 'type' in bldg_features.keys():
                if bldg_features['type'] not in ["building", "bridge"]:
                    raise Exception(
                        "The csv file {file_path} cannot have a column named 'type'")
            else:
                bldg_features['type'] = str_type

            # is the id provided by user?
            if id_column == None:
                # if not we assin the id
                id = id_counter
            else:
                if id_column not in bldg_features.keys():
                    raise Exception(
                        "The key '{}' not found in {}".format(id_column, file_path))
                id = bldg_features[id_column]

            asset = Asset(id, coordinates, bldg_features)
            self.add_asset(id, asset)
            id_counter += 1

        return True

    def add_asset_features_from_csv(self, file_path, id_column) -> bool:
        """
        Read inventory data from a CSV file and add it to the inventory.

        Args:
            file_path (str):
                  The path to the CSV file
            id_column (str):
                  The name of column that contains id values. If None, new indicies will be assigned

        Returns:
            bool:
                  True if assets were addded, False otherwise.
        """

        try:  # Attempt to open the file
            with open(file_path, mode="r") as csvfile:
                csv_reader = csv.DictReader(csvfile)
                rows = list(csv_reader)
        except FileNotFoundError:
            raise Exception("The file {} does not exist.".format(csvfile))

        for bldg_features in rows:
            for i, key in enumerate(bldg_features):
                # converting to number
                val = bldg_features[key]
                if val.isdigit():
                    bldg_features[key] = int(val)
                elif InputValidator.is_float(val):
                    bldg_features[key] = float(val)

            if id_column not in bldg_features.keys():
                raise Exception(
                    "The key '{}' not found in {}".format(id_column, file_path))
            id = bldg_features[id_column]

            self.add_asset_features(id, bldg_features)

        return True

    def get_dataframe(self, n_possible_worlds=1, features_possible_worlds=[]) -> bool:
        """
        Read inventory data from a CSV file and add it to the inventory.

        Args:
            n_possible_worlds (int):
                  Number of possible worlds
            features_possible_worlds (list of str):
                  Indicate the features with multiple possible worlds

        Returns:
            bool:
                  True if assets were addded, False otherwise.
        """

        features_json = self.get_geojson()['features']
        bldg_properties = [(self.inventory[i].features | {
            "index": i}) for dummy, i in enumerate(self.inventory)]

        # [bldg_features['properties'] for bldg_features in features_json]

        nbldg = len(bldg_properties)

        if n_possible_worlds == 1:
            bldg_properties_df = pd.DataFrame(bldg_properties)

        else:
            # First enumerate assets to see which columns have multiple worlds

            vector_columns = set()
            for entry in bldg_properties:
                vector_columns.update(
                    [key for key, value in entry.items() if isinstance(value, list)])

            flat_data = []
            for entry in bldg_properties:
                row = {key: value for key, value in entry.items() if (
                    key not in vector_columns)}  # stays the same
                for key in vector_columns:
                    value = entry[key]
                    if isinstance(value, list):
                        if not len(value) == n_possible_worlds:
                            raise ValueError("The specified # of possible worlds are {} but {} constains {} realizations in {}".format(
                                n_possible_worlds, key, len(value), entry))

                        for i in range(n_possible_worlds):
                            row[f'{key}_{i+1}'] = value[i]
                    else:
                        for i in range(n_possible_worlds):
                            row[f'{key}_{i+1}'] = value

                flat_data.append(row)

            bldg_properties_df = pd.DataFrame(flat_data)

        bldg_properties_df.drop(columns=['type'], inplace=True)

        #  get centoried
        lat_values = [None] * nbldg
        lon_values = [None] * nbldg
        for idx in range(nbldg):
            polygon_coordinate = features_json[idx]['geometry']['coordinates']
            latitudes = [coord[1] for coord in polygon_coordinate]
            longitudes = [coord[0] for coord in polygon_coordinate]
            lat_values[idx] = sum(latitudes) / len(latitudes)
            lon_values[idx] = sum(longitudes) / len(longitudes)

        # to be used for spatial interpolation
        # lat_values = [features_json[idx]['geometry']['coordinates'][0][0] for idx in range(nbldg)]
        # lon_values = [features_json[idx]['geometry']['coordinates'][0][1] for idx in range(nbldg)]
        bldg_geometries_df = pd.DataFrame()
        bldg_geometries_df["Lat"] = lat_values
        bldg_geometries_df["Lon"] = lon_values
        bldg_geometries_df["index"] = bldg_properties_df["index"]

        bldg_properties_df = bldg_properties_df.set_index("index")
        bldg_geometries_df = bldg_geometries_df.set_index("index")

        return bldg_properties_df, bldg_geometries_df, nbldg
