import json
import ast  # Used for safer evaluation
from datetime import datetime

class Inventory:
    """Manages the stock, data loading, and reporting for an inventory system."""

    def __init__(self, stock_data=None):
        """Initializes the inventory with optional starting stock."""
        self.stock_data = stock_data if stock_data is not None else {}

    def add_item(self, item="default", qty=0, logs=None):
        """Adds quantity to an item's stock."""
        # FIX: Dangerous default value
        if logs is None:
            logs = []
        
        if not item:
            return
        
        # FIX: Missing Type Validation
        if not isinstance(qty, (int, float)):
            return
            
        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        
        # FIX: Using old string formatting
        logs.append(f"{datetime.now()}: Added {qty} of {item}")

    def remove_item(self, item, qty):
        """Removes quantity from an item's stock."""
        try:
            self.stock_data[item] -= qty
            if self.stock_data[item] <= 0:
                del self.stock_data[item]
        # FIX: Bare except with pass
        except KeyError:
            pass

    def get_qty(self, item):
        """Returns the current quantity of an item."""
        return self.stock_data.get(item) # Using .get() is safer than direct access

    def load_data(self, file="inventory.json"):
        """Loads inventory data from a JSON file."""
        # FIX: Not using 'with' and Unspecified encoding
        try:
            with open(file, "r", encoding="utf-8") as f:
                self.stock_data = json.loads(f.read())
        except FileNotFoundError:
            # Handle the case where the file doesn't exist yet
            self.stock_data = {}
        except json.JSONDecodeError:
            # Handle case where file is corrupt
            self.stock_data = {}

    def save_data(self, file="inventory.json"):
        """Saves current inventory data to a JSON file."""
        # FIX: Not using 'with' and Unspecified encoding
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.stock_data))

    def print_data(self):
        """Prints a report of all items and their quantities."""
        print("Items Report")
        for i, qty in self.stock_data.items():
            print(i, "->", qty)

    def check_low_items(self, threshold=5):
        """Returns a list of items below the stock threshold."""
        result = []
        for i in self.stock_data:
            if self.stock_data[i] < threshold:
                result.append(i)
        return result

# --- Main execution ---
def main():
    # Instantiate the inventory system (no need for global stock_data)
    inventory = Inventory()
    
    inventory.add_item("apple", 10)
    inventory.add_item("banana", -2)
    # This call is now safely ignored due to type checking
    inventory.add_item(123, "ten") 
    
    inventory.remove_item("apple", 3)
    inventory.remove_item("orange", 1) # Safely handled due to KeyError fix
    
    print("Apple stock:", inventory.get_qty("apple"))
    print("Low items:", inventory.check_low_items())
    
    inventory.save_data()
    inventory.load_data()
    inventory.print_data()
    
    # FIX: Use of eval removed. Example of safe evaluation:
    # safe_data = ast.literal_eval('{"key": 1, "value": 2}') 

if __name__ == '__main__':
    main()
