import pytest
from pydantic import ValidationError
from backend.schemas.seed import EnvironmentProfile

def test_valid_payload_parsing():
    data = {
        "name": "pytorch-cuda-12.1",
        "framework": "pytorch",
        "cuda_version": "12.1"
    }
    request = EnvironmentProfile(**data)
    assert request.name == "pytorch-cuda-12.1"
    assert request.framework == "pytorch"
    assert request.cuda_version == "12.1"

def test_invalid_target_os_raises_error():
    # Testing an invalid configuration setup
    data = {
        "name": "invalid-profile",
        "framework": "invalid_framework",
        "cuda_version": "12.1"
    }
    with pytest.raises(ValidationError):
        EnvironmentProfile(**data)

def test_invalid_data_types_raises_error():
    # Requirement 2: Testing an incorrect data type (integer instead of string)
    data = {
        "name": 12345,
        "framework": "pytorch",
        "cuda_version": "12.1"
    }
    with pytest.raises(ValidationError):
        EnvironmentProfile(**data)

def test_missing_required_fields_raises_error():
    # Requirement 2: Testing missing mandatory fields
    data = {
        "cuda_version": "12.1"
    }
    with pytest.raises(ValidationError):
        EnvironmentProfile(**data)

def test_empty_payload_raises_error():
    with pytest.raises(ValidationError):
        EnvironmentProfile(**{})

def test_generation_request_empty_payload():
    """Requirement 3: Ensures an empty payload raises a ValidationError gracefully"""
    with pytest.raises(ValidationError):
        EnvironmentProfile(**{})
        
