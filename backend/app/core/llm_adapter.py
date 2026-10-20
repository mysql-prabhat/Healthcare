def call_llm_mock(context: dict) -> dict:
    return {
        "summary": "Mock: patient with cough and fever",
        "actions": [{"type":"order_lab","code":"CBC"},{"type":"schedule","days":3}],
        "confidence": 0.95
    }