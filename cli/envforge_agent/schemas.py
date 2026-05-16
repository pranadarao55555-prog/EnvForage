"""
Pydantic data models for the DiagnosticReport.

These models are kept in sync with the backend's:
  backend/app/schemas/diagnostic.py

The CLI agent uses these models to validate its own output before
writing to stdout or sending to the API.

IMPORTANT: The JSON output of these models IS the API request body for
POST /api/v1/diagnose. Any field change here requires a corresponding
change in the backend schema.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class OSInfo(BaseModel):
    name: str                        # e.g. "Windows 11", "Ubuntu 22.04"
    version: str                     # e.g. "22.04", "10.0.22631"
    architecture: str                # e.g. "x86_64", "AMD64"
    wsl_version: str | None = None   # e.g. "WSL2", None if not WSL


class CPUInfo(BaseModel):
    brand: str                       # e.g. "Intel Core i9-13900K"
    cores: int                       # Physical cores
    threads: int                     # Logical threads (with HT)


class RAMInfo(BaseModel):
    total_gb: float
    available_gb: float


class GPUInfo(BaseModel):
    name: str                        # e.g. "NVIDIA RTX 4090"
    vram_gb: float | None = None     # VRAM in GB
    driver_version: str | None = None
    index: int = 0                   # 0-based GPU index (multi-GPU systems)


class CUDAInfo(BaseModel):
    version: str | None = None       # e.g. "12.1"
    toolkit_path: str | None = None  # e.g. "/usr/local/cuda-12.1"
    cudnn_version: str | None = None # e.g. "8.9.0"
    nccl_version: str | None = None


class ROCMInfo(BaseModel):
    version: str | None = None       # e.g. "5.6"
    gcn_arch: str | None = None      # e.g. "gfx1030"


class PythonInfo(BaseModel):
    version: str                     # e.g. "3.11.9"
    path: str                        # Absolute path to python executable
    is_venv: bool = False
    venv_path: str | None = None     # Path to venv root if is_venv
    pip_version: str | None = None   # e.g. "24.0"


class DiagnosticReport(BaseModel):
    """
    Structured diagnostic report produced by the CLI agent.

    This is both the CLI output format and the POST /api/v1/diagnose request body.
    Fields must remain in sync with backend/app/schemas/diagnostic.py.
    """
    agent_version: str = Field("0.1.0", description="envforge-agent version")
    os: OSInfo
    cpu: CPUInfo
    ram: RAMInfo
    gpus: list[GPUInfo] = Field(default_factory=list)
    cuda: CUDAInfo = Field(default_factory=CUDAInfo)
    rocm: ROCMInfo = Field(default_factory=ROCMInfo)
    python_installations: list[PythonInfo] = Field(default_factory=list)
    active_python: PythonInfo | None = None

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string (API-compatible)."""
        return self.model_dump_json(indent=indent)
