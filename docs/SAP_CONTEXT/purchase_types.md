# PURCHASE TYPES

```json
[
  {
    "purchase_type": "SPOT",
    "purchase_document_type": "NB",
    "description": "One-time procurement without an existing contract or long-term agreement.",
    "typical_use_cases": [
      "Urgent purchases",
      "Exceptional demand",
      "Low-frequency procurement",
      "Ad-hoc material requests"
    ],
    "signals_in_text": [
      "urgent",
      "only once",
      "one-time purchase",
      "immediate need",
      "temporary demand",
      "emergency purchase"
    ],
    "procurement_characteristics": {
      "contract_based": false,
      "planning_based": false,
      "inventory_related": true,
      "requires_supplier_selection": true
    }
  },
  {
    "purchase_type": "PLANNED",
    "purchase_document_type": "ZMRP",
    "description": "Procurement generated automatically through MRP or planning processes.",
    "typical_use_cases": [
      "Stock replenishment",
      "Forecast-based procurement",
      "Automatic purchasing",
      "Production planning support"
    ],
    "signals_in_text": [
      "automatic requisition",
      "replenishment",
      "minimum stock",
      "reorder point",
      "forecast",
      "MRP",
      "planned demand",
      "safety stock"
    ],
    "procurement_characteristics": {
      "contract_based": false,
      "planning_based": true,
      "inventory_related": true,
      "automatic_generation": true
    }
  },
  {
    "purchase_type": "CONTRACT",
    "purchase_document_type": "ZCPO",
    "description": "Procurement executed against an existing contract or scheduling agreement.",
    "typical_use_cases": [
      "Framework agreements",
      "Long-term supplier contracts",
      "Scheduled releases",
      "Recurring purchases"
    ],
    "signals_in_text": [
      "contract number",
      "agreement",
      "release",
      "scheduling agreement",
      "SA",
      "contract release",
      "framework agreement"
    ],
    "procurement_characteristics": {
      "contract_based": true,
      "planning_based": false,
      "inventory_related": true,
      "requires_existing_contract": true
    }
  },
  {
    "purchase_type": "SERVICE",
    "purchase_document_type": "ZSPO",
    "description": "Procurement of services rather than physical materials.",
    "typical_use_cases": [
      "Consulting services",
      "Maintenance contracts",
      "Technical support",
      "Professional services"
    ],
    "signals_in_text": [
      "work labor",
      "consultants",
      "consulting",
      "maintenance",
      "technical support",
      "installation",
      "training",
      "service execution",
      "hourly rate"
    ],
    "procurement_characteristics": {
      "contract_based": true,
      "planning_based": false,
      "inventory_related": false,
      "service_based": true,
      "may_not_require_materials": true
    }
  },
  {
    "purchase_type": "STO",
    "purchase_document_type": "UB",
    "description": "Internal stock transfer between plants or storage locations within the same company.",
    "typical_use_cases": [
      "Plant replenishment",
      "Internal logistics",
      "Stock redistribution",
      "Inter-plant transfer"
    ],
    "signals_in_text": [
      "transfer",
      "destination plant",
      "origin plant",
      "supplying plant",
      "plant",
      "internal movement",
      "same CNPJ",
      "stock transfer"
    ],
    "procurement_characteristics": {
      "contract_based": false,
      "planning_based": true,
      "inventory_related": true,
      "internal_procurement": true
    }
  },
  {
    "purchase_type": "SUBCONTRACTING",
    "purchase_document_type": "ZTPO",
    "description": "Procurement process where components are provided to a third party for industrial processing or assembly.",
    "typical_use_cases": [
      "Industrial processing",
      "Refining",
      "Assembly operations",
      "External manufacturing"
    ],
    "signals_in_text": [
      "processing",
      "refining",
      "beneficiation",
      "industrialization",
      "components",
      "third party",
      "assembly",
      "send components"
    ],
    "procurement_characteristics": {
      "contract_based": true,
      "planning_based": true,
      "inventory_related": true,
      "requires_component_supply": true,
      "third_party_processing": true
    }
  },
  {
    "purchase_type": "CONSIGNMENT",
    "purchase_document_type": "ZCPO",
    "description": "Procurement model where inventory remains vendor-owned until consumption.",
    "typical_use_cases": [
      "Vendor managed inventory",
      "Strategic stock agreements",
      "High-volume consumables",
      "Consigned stock"
    ],
    "signals_in_text": [
      "consigned",
      "payment for consumption",
      "consigned stock",
      "billed at sales",
      "vendor-owned inventory",
      "consumption-based billing"
    ],
    "procurement_characteristics": {
      "contract_based": true,
      "planning_based": true,
      "inventory_related": true,
      "ownership_transferred_after_consumption": true
    }
  }
]
```
