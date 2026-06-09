```json
[
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
```