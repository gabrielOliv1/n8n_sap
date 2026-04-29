from app.domain.enums.purchase_type import PurchaseType
from app.domain.schemas.llm_classification import LLMClassificationOutput


def test_schema_instantiation():
    output = LLMClassificationOutput(
        purchase_type=PurchaseType.SPOT,
        item_category="TI",
        material="Notebook",
        quantity=1,
        price=5000.0,
        uom="UN",
        supplier="Dell",
        plant="SP",
        buying_model="Direct",
        recommended_flow="Standard",
    )
    assert output.purchase_type == PurchaseType.SPOT
    assert output.price == 5000.0
