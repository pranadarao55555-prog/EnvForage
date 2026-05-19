import pytest
from pydantic import ValidationError
from backend.schemas.seed import GenerationRequest 

def test_generation_request_valid_data():
    """Verifies valid data parses successfully through the model"""
    valid_payload = {
        "target_os": "linux",
        "framework": "pytorch",
        "cuda_version": "12.1"
    }
    request = GenerationRequest(**valid_payload)
    assert request.target_os == "linux"
    assert request.framework == "pytorch"

def test_generation_request_invalid_os():
    """Catches a ValidationError when an invalid target_os value is passed"""
    invalid_payload = {
        "target_os": "invalid_operating_system",
        "framework": "pytorch",
        "cuda_version": "12.1"
    }
    with pytest.raises(ValidationError):
        GenerationRequest(**invalid_payload)

def test_generation_request_missing_fields():
    """Catches a ValidationError when mandatory payload fields are missing"""
    incomplete_payload = {
        "cuda_version": "12.1"
    }
    with pytest.raises(ValidationError):
        GenerationRequest(**incomplete_payload)
      
