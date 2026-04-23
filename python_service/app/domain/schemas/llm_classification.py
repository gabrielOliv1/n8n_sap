from pydantic import BaseModel
from app.domain.enums.purchase_type import PurchaseType

class LLMClassificationOutput(BaseModel):
    purchase_type: PurchaseType
    item_category: str
    material: str
    quantity: int
    price: float
    uom: str
    supplier: str
    plant: str
    buying_model: str
    recommended_flow: str
