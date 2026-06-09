# ITEM CATEGORIES

The item category determines together with other settings, for example in the material master, the following:

- The procurement type
    
- In which kinds of stock the material can be managed
    
- The account assignment category

```json
[
  {
    "item_category": "STANDARD",
    "sap_code": "",
    "description": "Standard procurement of physical goods or materials with defined quantities.",
    "typical_use_cases": [
      "Raw materials",
      "Finished goods",
      "Consumables",
      "Stock replenishment"
    ],
    "signals_in_text": [
      "material",
      "SAP material code",
      "stock",
      "replenishment",
      "defined quantity",
      "inventory",
      "warehouse",
      "purchase quantity"
    ],
    "procurement_characteristics": {
      "physical_goods": true,
      "service_based": false,
      "inventory_managed": true,
      "quantity_defined": true
    }
  },
  {
    "item_category": "SERVICE",
    "sap_code": "D",
    "description": "Procurement of services rather than physical materials.",
    "typical_use_cases": [
      "Consulting",
      "Maintenance",
      "Technical support",
      "Cleaning services",
      "Training"
    ],
    "signals_in_text": [
      "service",
      "consulting",
      "consultant",
      "maintenance",
      "cleaning",
      "repairs",
      "installation",
      "training",
      "technical support",
      "hour rate",
      "execute",
      "develop",
      "Service Entry Sheet",
      "SES"
    ],
    "procurement_characteristics": {
      "physical_goods": false,
      "service_based": true,
      "inventory_managed": false,
      "requires_service_entry_sheet": true
    }
  },
  {
    "item_category": "LIMIT",
    "sap_code": "B",
    "description": "Procurement with a predefined budget limit instead of fixed quantities.",
    "typical_use_cases": [
      "Framework agreements",
      "Variable demand consumables",
      "Catalog purchases",
      "Emergency purchases"
    ],
    "signals_in_text": [
      "budget up to",
      "limit value",
      "from",
      "to",
      "catalog",
      "upon variable demand",
      "flexible consumable",
      "umbrella agreement"
    ],
    "procurement_characteristics": {
      "physical_goods": true,
      "service_based": true,
      "inventory_managed": false,
      "quantity_defined": false,
      "budget_controlled": true
    }
  },
  {
    "item_category": "CONSIGNMENT",
    "sap_code": "K",
    "description": "Vendor-owned inventory stored at company premises until consumption.",
    "typical_use_cases": [
      "Vendor-managed inventory",
      "Strategic stock agreements",
      "High-volume consumables"
    ],
    "signals_in_text": [
      "vendor-owned inventory",
      "consigned",
      "consigned stock",
      "liability after consumption",
      "vendor managed inventory"
    ],
    "procurement_characteristics": {
      "physical_goods": true,
      "service_based": false,
      "inventory_managed": true,
      "ownership_transferred_after_consumption": true
    }
  },
  {
    "item_category": "SUBCONTRACTING",
    "sap_code": "L",
    "description": "Components are provided to a vendor who performs processing and returns a finished or semi-finished product.",
    "typical_use_cases": [
      "Industrial processing",
      "External manufacturing",
      "Assembly operations",
      "Refining"
    ],
    "signals_in_text": [
      "industrialization",
      "BOM",
      "Bill of Materials",
      "components",
      "send components",
      "processing",
      "refining",
      "finished products"
    ],
    "procurement_characteristics": {
      "physical_goods": true,
      "service_based": true,
      "requires_components_supply": true,
      "requires_bom": true
    }
  },
  {
    "item_category": "STOCK_TRANSFER",
    "sap_code": "U",
    "description": "Internal transfer of materials between plants or storage locations within the company.",
    "typical_use_cases": [
      "Intercompany transfer",
      "Plant replenishment",
      "Internal logistics",
      "Stock redistribution"
    ],
    "signals_in_text": [
      "transfer",
      "between plants",
      "internal plants",
      "supplying plant",
      "internal movement",
      "stock redistribution"
    ],
    "procurement_characteristics": {
      "physical_goods": true,
      "service_based": false,
      "internal_procurement": true,
      "inventory_managed": true
    }
  }
]
```