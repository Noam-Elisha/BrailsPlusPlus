from abc import ABC, abstractmethod
from brails.types.asset_inventory import AssetInventory


class Imputation(ABC):
    """
    Abstract base class representing a class that uses data imputation to fill in missing data

      Methods:
         imputate(inventory): An abstract method to fill in the missing features in an AssetInvetory

    """

    @abstractmethod
    def imputate(self, inventory: AssetInventory): 
        """
        Imputate an Asset Inventory

            Args:
                inventory (AssetInventory): the inventory
        """
        pass
