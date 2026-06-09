

```json const flows = [
  {
    "flow_id": "PR_TO_PO",
    "flow_name": "Purchase Requisition to Purchase Order",
    "process_category": "STANDARD_PROCUREMENT",
    "description": "Standard procurement flow where a Purchase Requisition (PR) is manually or automatically created and later converted into a Purchase Order (PO).",
    "typical_use_cases": [
      "Routine material purchases",
      "Department requests",
      "Operational procurement",
      "Stock replenishment"
    ],
    "when_to_use": [
      "A business area requests materials or services",
      "The supplier is already known",
      "No quotation process is required",
      "The company follows approval workflows before purchasing"
    ],
    "main_documents": [
      "Purchase Requisition",
      "Purchase Order"
    ],
    "sap_document_types": [
      "NB"
    ],
    "typical_item_categories": [
      "STANDARD",
      "SERVICE"
    ],
    "signals_in_text": [
      "purchase request",
      "need material",
      "request approval",
      "create PO",
      "requisition"
    ],
    "business_characteristics": {
      "requires_approval": true,
      "requires_supplier_selection": true,
      "supports_inventory_management": true,
      "contract_based": false
    }
  },
  {
    "flow_id": "MRP_TO_PO",
    "flow_name": "MRP Generated Procurement",
    "process_category": "PLANNED_PROCUREMENT",
    "description": "Procurement flow triggered automatically by MRP (Material Requirements Planning) based on stock levels, forecast, or production demand.",
    "typical_use_cases": [
      "Automatic replenishment",
      "Production planning",
      "Safety stock replenishment",
      "Recurring operational materials"
    ],
    "when_to_use": [
      "Stock levels fall below reorder point",
      "Demand forecast requires replenishment",
      "MRP execution generates planned procurement proposals"
    ],
    "main_documents": [
      "Planned Order",
      "Purchase Requisition",
      "Purchase Order"
    ],
    "sap_document_types": [
      "ZMRP"
    ],
    "typical_item_categories": [
      "STANDARD",
      "SUBCONTRACTING"
    ],
    "signals_in_text": [
      "MRP",
      "forecast",
      "reorder point",
      "automatic requisition",
      "minimum stock",
      "planned procurement"
    ],
    "business_characteristics": {
      "requires_approval": false,
      "automatically_generated": true,
      "inventory_driven": true,
      "planning_based": true
    }
  },
  {
    "flow_id": "RFQ_TO_PO",
    "flow_name": "Request for Quotation to Purchase Order",
    "process_category": "STRATEGIC_SOURCING",
    "description": "Procurement process where quotations are requested from multiple suppliers before selecting and creating a Purchase Order.",
    "typical_use_cases": [
      "Competitive sourcing",
      "High-value purchases",
      "New supplier evaluation",
      "Strategic procurement"
    ],
    "when_to_use": [
      "Price comparison is required",
      "Supplier competition is desired",
      "Procurement policy requires quotations",
      "Large-value acquisitions"
    ],
    "main_documents": [
      "Purchase Requisition",
      "RFQ",
      "Quotation",
      "Purchase Order"
    ],
    "sap_document_types": [
      "NB",
      "AN" 
    ],
    "typical_item_categories": [
      "STANDARD",
      "SERVICE"
    ],
    "signals_in_text": [
      "quotation",
      "proposal",
      "commercial offer",
      "best price",
      "supplier comparison",
      "RFQ"
    ],
    "business_characteristics": {
      "requires_approval": true,
      "requires_supplier_comparison": true,
      "strategic_sourcing": true,
      "contract_based": false
    }
  },
  {
    "flow_id": "CONTRACT_TO_RELEASE_ORDER",
    "flow_name": "Contract Release Procurement",
    "process_category": "CONTRACT_PROCUREMENT",
    "description": "Procurement process where Purchase Orders are created referencing an existing contract or scheduling agreement.",
    "typical_use_cases": [
      "Recurring purchases",
      "Long-term agreements",
      "Framework contracts",
      "Negotiated supplier agreements"
    ],
    "when_to_use": [
      "An active contract already exists",
      "Pricing and terms are pre-negotiated",
      "Recurring procurement occurs frequently"
    ],
    "main_documents": [
      "Contract",
      "Release Order",
      "Purchase Order"
    ],
    "sap_document_types": [
      "MK",
      "WK",
      "ZCPO"
    ],
    "typical_item_categories": [
      "STANDARD",
      "SERVICE",
      "CONSIGNMENT"
    ],
    "signals_in_text": [
      "contract number",
      "release order",
      "agreement",
      "scheduled delivery",
      "framework agreement"
    ],
    "business_characteristics": {
      "requires_existing_contract": true,
      "negotiated_conditions": true,
      "supports_recurring_procurement": true,
      "contract_based": true
    }
  },
  {
    "flow_id": "SERVICE_PO_TO_SES_TO_INVOICE",
    "flow_name": "Service Procurement with SES",
    "process_category": "SERVICE_PROCUREMENT",
    "description": "Service procurement flow where services are confirmed through a Service Entry Sheet (SES) before invoice processing.",
    "typical_use_cases": [
      "Consulting services",
      "Maintenance contracts",
      "Technical support",
      "Outsourced labor"
    ],
    "when_to_use": [
      "Services require execution confirmation",
      "Payment depends on service acceptance",
      "The procurement involves labor or expertise instead of materials"
    ],
    "main_documents": [
      "Purchase Order",
      "Service Entry Sheet",
      "Invoice"
    ],
    "sap_document_types": [
      "ZSPO"
    ],
    "typical_item_categories": [
      "SERVICE",
      "LIMIT"
    ],
    "signals_in_text": [
      "service entry sheet",
      "SES",
      "consulting",
      "maintenance",
      "hourly rate",
      "service execution"
    ],
    "business_characteristics": {
      "requires_service_confirmation": true,
      "service_based": true,
      "inventory_related": false,
      "invoice_after_acceptance": true
    }
  },
  {
    "flow_id": "STO_TO_DELIVERY_TO_GR",
    "flow_name": "Stock Transport Order Process",
    "process_category": "INTERNAL_LOGISTICS",
    "description": "Internal material transfer process between plants or storage locations using a Stock Transport Order (STO).",
    "typical_use_cases": [
      "Inter-plant replenishment",
      "Internal logistics",
      "Warehouse balancing",
      "Stock redistribution"
    ],
    "when_to_use": [
      "Materials must be transferred internally",
      "The supplying and receiving plants belong to the same organization",
      "No external supplier is involved"
    ],
    "main_documents": [
      "Stock Transport Order",
      "Outbound Delivery",
      "Goods Receipt"
    ],
    "sap_document_types": [
      "UB"
    ],
    "typical_item_categories": [
      "STOCK_TRANSFER"
    ],
    "signals_in_text": [
      "internal transfer",
      "supplying plant",
      "receiving plant",
      "stock movement",
      "plant transfer"
    ],
    "business_characteristics": {
      "internal_procurement": true,
      "requires_delivery_document": true,
      "inventory_related": true,
      "external_supplier": false
    }
  },
  {
    "flow_id": "DIRECT_PO",
    "flow_name": "Direct Purchase Order",
    "process_category": "SIMPLIFIED_PROCUREMENT",
    "description": "Simplified procurement process where a Purchase Order is created directly without a preceding Purchase Requisition.",
    "typical_use_cases": [
      "Urgent purchases",
      "Low-value procurement",
      "Operational emergencies",
      "Fast-track acquisitions"
    ],
    "when_to_use": [
      "Immediate procurement is required",
      "Approval steps are simplified",
      "The buyer has authority to create PO directly"
    ],
    "main_documents": [
      "Purchase Order"
    ],
    "sap_document_types": [
      "NB"
    ],
    "typical_item_categories": [
      "STANDARD",
      "SERVICE"
    ],
    "signals_in_text": [
      "urgent",
      "immediate purchase",
      "direct PO",
      "emergency",
      "buy immediately"
    ],
    "business_characteristics": {
      "requires_requisition": false,
      "fast_execution": true,
      "simplified_approval": true,
      "contract_based": false
    }
  }
]
const item_categories = [
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
const materials = [
  {
    "material_code": "RM-100001",
    "short_text": "Hot Rolled Steel Sheet",
    "material_type_code": "ROH",
    "material_type_description": "Raw Material"
  },
  {
    "material_code": "RM-100002",
    "short_text": "Industrial Grade Lubricant Oil",
    "material_type_code": "ROH",
    "material_type_description": "Raw Material"
  },
  {
    "material_code": "SF-200001",
    "short_text": "Semi-Finished Aluminum Frame",
    "material_type_code": "HALB",
    "material_type_description": "Semi-Finished Material"
  },
  {
    "material_code": "FG-300001",
    "short_text": "Hydraulic Pump Assembly",
    "material_type_code": "FERT",
    "material_type_description": "Finished Product"
  },
  {
    "material_code": "FG-300002",
    "short_text": "Industrial Control Panel",
    "material_type_code": "FERT",
    "material_type_description": "Finished Product"
  },
  {
    "material_code": "SP-400001",
    "short_text": "Ball Bearing 6205-ZZ",
    "material_type_code": "ERSA",
    "material_type_description": "Spare Part"
  },
  {
    "material_code": "SP-400002",
    "short_text": "Hydraulic Seal Kit",
    "material_type_code": "ERSA",
    "material_type_description": "Spare Part"
  },
  {
    "material_code": "SP-400003",
    "short_text": "Electric Motor Cooling Fan",
    "material_type_code": "ERSA",
    "material_type_description": "Spare Part"
  },
  {
    "material_code": "TR-500001",
    "short_text": "Forklift Rental Service",
    "material_type_code": "DIEN",
    "material_type_description": "Service"
  },
  {
    "material_code": "TR-500002",
    "short_text": "Preventive Maintenance Service",
    "material_type_code": "DIEN",
    "material_type_description": "Service"
  },
  {
    "material_code": "TR-500003",
    "short_text": "IT Infrastructure Consulting",
    "material_type_code": "DIEN",
    "material_type_description": "Service"
  },
  {
    "material_code": "PK-600001",
    "short_text": "Wooden Export Pallet",
    "material_type_code": "VERP",
    "material_type_description": "Packaging Material"
  },
  {
    "material_code": "PK-600002",
    "short_text": "Corrugated Cardboard Box",
    "material_type_code": "VERP",
    "material_type_description": "Packaging Material"
  },
  {
    "material_code": "CO-700001",
    "short_text": "Safety Gloves Size L",
    "material_type_code": "HIBE",
    "material_type_description": "Operating Supplies"
  },
  {
    "material_code": "CO-700002",
    "short_text": "Industrial Cleaning Solvent",
    "material_type_code": "HIBE",
    "material_type_description": "Operating Supplies"
  }
]
const purchase_types = [
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
const suppliers = [
  {
    "supplier_id": "SUP-1001",
    "supplier_name": "Global Industrial Metals Ltd",
    "supplier_type": "RAW_MATERIAL",
    "country": "Brazil",
    "city": "Sao Paulo",
    "currency": "BRL",
    "preferred_language": "pt",
    "payment_terms": "NET30",
    "incoterm": "FOB",
    "known_categories": [
      "STANDARD",
      "SUBCONTRACTING"
    ],
    "known_material_types": [
      "ROH",
      "HALB"
    ],
    "typical_signals": [
      "steel",
      "aluminum",
      "raw material",
      "industrial processing"
    ],
    "supports_contracts": true,
    "supports_scheduling_agreement": true,
    "is_internal_company": false
  },
  {
    "supplier_id": "SUP-1002",
    "supplier_name": "TechSource Consulting Group",
    "supplier_type": "SERVICE_PROVIDER",
    "country": "United States",
    "city": "Austin",
    "currency": "USD",
    "preferred_language": "en",
    "payment_terms": "NET15",
    "incoterm": null,
    "known_categories": [
      "SERVICE"
    ],
    "known_material_types": [
      "DIEN"
    ],
    "typical_signals": [
      "consulting",
      "technical support",
      "implementation",
      "hourly rate"
    ],
    "supports_contracts": true,
    "supports_scheduling_agreement": false,
    "is_internal_company": false
  },
  {
    "supplier_id": "SUP-1003",
    "supplier_name": "Prime Maintenance Services",
    "supplier_type": "MAINTENANCE_SERVICE",
    "country": "Brazil",
    "city": "Campinas",
    "currency": "BRL",
    "preferred_language": "pt",
    "payment_terms": "NET30",
    "incoterm": null,
    "known_categories": [
      "SERVICE",
      "LIMIT"
    ],
    "known_material_types": [
      "DIEN"
    ],
    "typical_signals": [
      "maintenance",
      "cleaning",
      "repair",
      "service entry sheet"
    ],
    "supports_contracts": true,
    "supports_scheduling_agreement": true,
    "is_internal_company": false
  },
  {
    "supplier_id": "SUP-1004",
    "supplier_name": "Internal Plant North",
    "supplier_type": "INTERNAL_PLANT",
    "country": "Brazil",
    "city": "Manaus",
    "currency": "BRL",
    "preferred_language": "pt",
    "payment_terms": null,
    "incoterm": null,
    "known_categories": [
      "STOCK_TRANSFER"
    ],
    "known_material_types": [
      "FERT",
      "ROH"
    ],
    "typical_signals": [
      "supplying plant",
      "internal transfer",
      "plant transfer",
      "stock redistribution"
    ],
    "supports_contracts": false,
    "supports_scheduling_agreement": false,
    "is_internal_company": true
  },
  {
    "supplier_id": "SUP-1005",
    "supplier_name": "Precision Spare Parts GmbH",
    "supplier_type": "SPARE_PARTS",
    "country": "Germany",
    "city": "Hamburg",
    "currency": "EUR",
    "preferred_language": "en",
    "payment_terms": "NET45",
    "incoterm": "CIF",
    "known_categories": [
      "STANDARD",
      "CONSIGNMENT"
    ],
    "known_material_types": [
      "ERSA"
    ],
    "typical_signals": [
      "bearing",
      "seal kit",
      "replacement part",
      "consigned stock"
    ],
    "supports_contracts": true,
    "supports_scheduling_agreement": true,
    "is_internal_company": false
  },
  {
    "supplier_id": "SUP-1006",
    "supplier_name": "FlexPack Packaging Solutions",
    "supplier_type": "PACKAGING_SUPPLIER",
    "country": "Mexico",
    "city": "Monterrey",
    "currency": "USD",
    "preferred_language": "es",
    "payment_terms": "NET30",
    "incoterm": "EXW",
    "known_categories": [
      "STANDARD"
    ],
    "known_material_types": [
      "VERP"
    ],
    "typical_signals": [
      "packaging",
      "cardboard box",
      "pallet",
      "shipping material"
    ],
    "supports_contracts": true,
    "supports_scheduling_agreement": false,
    "is_internal_company": false
  },
  {
    "supplier_id": "SUP-1007",
    "supplier_name": "Alpha Chemicals Corporation",
    "supplier_type": "CHEMICAL_SUPPLIER",
    "country": "Brazil",
    "city": "Santos",
    "currency": "BRL",
    "preferred_language": "pt",
    "payment_terms": "NET60",
    "incoterm": "FOB",
    "known_categories": [
      "STANDARD",
      "CONSIGNMENT"
    ],
    "known_material_types": [
      "ROH",
      "HIBE"
    ],
    "typical_signals": [
      "solvent",
      "chemical",
      "bulk delivery",
      "vendor-owned inventory"
    ],
    "supports_contracts": true,
    "supports_scheduling_agreement": true,
    "is_internal_company": false
  },
  {
    "supplier_id": "SUP-1008",
    "supplier_name": "NextGen Manufacturing Partners",
    "supplier_type": "SUBCONTRACTOR",
    "country": "China",
    "city": "Shenzhen",
    "currency": "USD",
    "preferred_language": "en",
    "payment_terms": "NET45",
    "incoterm": "DAP",
    "known_categories": [
      "SUBCONTRACTING"
    ],
    "known_material_types": [
      "HALB",
      "FERT"
    ],
    "typical_signals": [
      "assembly",
      "processing",
      "industrialization",
      "send components"
    ],
    "supports_contracts": true,
    "supports_scheduling_agreement": true,
    "is_internal_company": false
  },
  {
    "supplier_id": "SUP-1009",
    "supplier_name": "Rapid Office Supplies",
    "supplier_type": "CONSUMABLES",
    "country": "Brazil",
    "city": "Curitiba",
    "currency": "BRL",
    "preferred_language": "pt",
    "payment_terms": "NET15",
    "incoterm": "CPT",
    "known_categories": [
      "LIMIT",
      "STANDARD"
    ],
    "known_material_types": [
      "HIBE"
    ],
    "typical_signals": [
      "catalog",
      "office supplies",
      "consumables",
      "flexible demand"
    ],
    "supports_contracts": false,
    "supports_scheduling_agreement": true,
    "is_internal_company": false
  },
  {
    "supplier_id": "SUP-1010",
    "supplier_name": "Enterprise IT Infrastructure Services",
    "supplier_type": "IT_SERVICE_PROVIDER",
    "country": "Canada",
    "city": "Toronto",
    "currency": "USD",
    "preferred_language": "en",
    "payment_terms": "NET30",
    "incoterm": null,
    "known_categories": [
      "SERVICE"
    ],
    "known_material_types": [
      "DIEN"
    ],
    "typical_signals": [
      "cloud migration",
      "IT infrastructure",
      "managed services",
      "technical consulting"
    ],
    "supports_contracts": true,
    "supports_scheduling_agreement": false,
    "is_internal_company": false
  }
]

return {
  context: `
## PROCUREMENT FLOWS
${JSON.stringify(flows, null, 2)}

## SUPPLIERS
${JSON.stringify(suppliers, null, 2)}

## PURCHASE TYPES
${JSON.stringify(purchase_types, null, 2)}

## MATERIALS
${JSON.stringify(materials, null, 2)}

## ITEM CATEGORIES
${JSON.stringify(item_categories, null, 2)}
  `.trim()
};```