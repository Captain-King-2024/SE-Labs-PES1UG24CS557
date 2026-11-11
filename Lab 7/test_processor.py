
from hypothesis import given, strategies as st, settings

from processor import (
    parse_season_pass_validity,
    compute_trail_gradient,
    calculate_lift_access_tier
)


# Test 1: Season Pass Validity
@settings(max_examples=200)
@given(st.text() | st.none())
def test_parse_season_pass_validity_no_crash(s):
    try:
        result = parse_season_pass_validity(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, (
            f"parse_season_pass_validity crashed "
            f"for input {s!r}: {e}"
        )


# Test 2: Trail Gradient
@settings(max_examples=200)
@given(st.text() | st.none())
def test_compute_trail_gradient_safe(s):
    try:
        result = compute_trail_gradient(s)
        assert isinstance(result, (int, float))
    except Exception as e:
        assert False, (
            f"compute_trail_gradient crashed "
            f"for input {s!r}: {e}"
        )


# Test 3: Lift Access Tier
@settings(max_examples=200)
@given(st.text() | st.none())
def test_calculate_lift_access_tier_safe(s):
    try:
        result = calculate_lift_access_tier(s)
        assert isinstance(result, (int, float))
    except Exception as e:
        assert False, (
            f"calculate_lift_access_tier crashed "
            f"for input {s!r}: {e}"
        )
