import pytest
from finance_governance.economics import ModelOption, estimate_inference_cost, compare_models, budget_gate

OPT = ModelOption("small", 0.001, 0.002)

def test_estimate_exact():
    assert estimate_inference_cost(OPT, 1000, 500, queries=10) == 0.02

def test_estimate_zero_queries_zero_variable_cost():
    assert estimate_inference_cost(OPT, 1000, 500, queries=0) == 0.0

def test_negative_input_tokens_rejected():
    with pytest.raises(ValueError):
        estimate_inference_cost(OPT, -1, 500)

def test_negative_output_tokens_rejected():
    with pytest.raises(ValueError):
        estimate_inference_cost(OPT, 1000, -5)

def test_negative_queries_rejected():
    with pytest.raises(ValueError):
        estimate_inference_cost(OPT, 1000, 500, queries=-2)

def test_negative_price_rejected():
    with pytest.raises(ValueError):
        ModelOption("bad", -0.01, 0.002)

def test_negative_fixed_rejected():
    with pytest.raises(ValueError):
        ModelOption("bad", 0.01, 0.002, fixed_monthly=-1)

def test_compare_sorts_cheapest_first():
    rows = compare_models([ModelOption("large", 0.01, 0.03), OPT], 1000, 500, queries=10)
    assert rows[0]["model"] == "small" and rows[1]["model"] == "large"

def test_budget_gate_pass_and_fail():
    assert budget_gate(50.0, 100.0) is True
    assert budget_gate(150.0, 100.0) is False

def test_budget_gate_negative_estimate_rejected():
    with pytest.raises(ValueError):
        budget_gate(-10.0, 100.0)

def test_budget_gate_negative_budget_rejected():
    with pytest.raises(ValueError):
        budget_gate(10.0, -100.0)
