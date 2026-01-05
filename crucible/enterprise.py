"""
Crucible Enterprise Features
============================

This module defines the boundary between open-core and enterprise features.

Open-Core (included):
- Training with curriculum learning
- Evaluation with tier-stratified metrics
- Capsule building with median selection
- Parameter sweeps
- Documentation and tooling

Enterprise (requires license):
- Organic adversarial miner (mine_tier3_organic)
- Capsule verification protocol
- Evidence chain generation
- Multi-seed automated optimization
- Priority support

To enable enterprise features, set CRUCIBLE_ENTERPRISE_KEY environment variable
or contact sales@example.com for a license.
"""

import os
from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T")

# Check for enterprise license
ENTERPRISE_KEY = os.environ.get("CRUCIBLE_ENTERPRISE_KEY", "")
ENTERPRISE_ENABLED = bool(ENTERPRISE_KEY and len(ENTERPRISE_KEY) > 16)


class EnterpriseFeatureError(Exception):
    """Raised when attempting to use an enterprise feature without a license."""

    def __init__(self, feature_name: str):
        self.feature_name = feature_name
        super().__init__(
            f"'{feature_name}' is an enterprise feature.\n"
            f"\n"
            f"This feature requires a Crucible Enterprise license.\n"
            f"Set CRUCIBLE_ENTERPRISE_KEY environment variable to enable.\n"
            f"\n"
            f"For licensing information, contact: sales@example.com\n"
            f"Documentation: docs/crucible/COMMERCIAL.md"
        )


def enterprise_feature(feature_name: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator that gates a function behind enterprise licensing.

    Usage:
        @enterprise_feature("organic_miner")
        def mine_organic_adversarials(...):
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            if not ENTERPRISE_ENABLED:
                raise EnterpriseFeatureError(feature_name)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_enterprise(feature_name: str) -> None:
    """
    Check if enterprise features are enabled.

    Usage:
        from crucible.enterprise import require_enterprise
        require_enterprise("capsule_verification")
        # ... enterprise code ...
    """
    if not ENTERPRISE_ENABLED:
        raise EnterpriseFeatureError(feature_name)


def is_enterprise_enabled() -> bool:
    """Check if enterprise features are available."""
    return ENTERPRISE_ENABLED


# =============================================================================
# Enterprise Feature Stubs
# =============================================================================
# These are placeholder implementations that raise EnterpriseFeatureError.
# The actual implementations would be in a separate private package.


@enterprise_feature("organic_miner")
def mine_organic_adversarials(
    checkpoint_path: str,
    corpus_path: str,
    output_path: str,
    threshold: float = 0.15,
    max_items: int = 1000,
) -> dict:
    """
    Mine organic adversarial examples from a corpus using a trained model.

    This identifies naturally-occurring hard cases where the model struggles,
    creating a diverse eval set that tests generalization.

    Args:
        checkpoint_path: Path to trained model checkpoint
        corpus_path: Path to unlabeled corpus for mining
        output_path: Where to write mined examples
        threshold: Margin threshold for "hard" classification
        max_items: Maximum items to mine

    Returns:
        Mining statistics (items found, tier distribution, etc.)
    """
    # Stub - actual implementation in enterprise package
    raise NotImplementedError("Enterprise implementation required")


@enterprise_feature("capsule_verification")
def verify_capsule(
    capsule_path: str,
    verification_key: str,
) -> dict:
    """
    Verify capsule integrity and generate evidence chain.

    Creates a cryptographic proof that the capsule was generated
    according to the specified recipe without tampering.

    Args:
        capsule_path: Path to capsule directory
        verification_key: Key for signing evidence

    Returns:
        Verification report with evidence chain
    """
    # Stub - actual implementation in enterprise package
    raise NotImplementedError("Enterprise implementation required")


@enterprise_feature("auto_optimization")
def run_automated_optimization(
    bundles_path: str,
    frozen_eval_path: str,
    organic_eval_path: str,
    budget_hours: float = 24.0,
) -> dict:
    """
    Run automated hyperparameter optimization with early stopping.

    Uses Bayesian optimization to find optimal tier3 ratios, learning rate,
    and training steps within a compute budget.

    Args:
        bundles_path: Training data
        frozen_eval_path: Frozen eval for retention
        organic_eval_path: Organic eval for generalization
        budget_hours: Maximum compute time

    Returns:
        Optimization results with best configuration
    """
    # Stub - actual implementation in enterprise package
    raise NotImplementedError("Enterprise implementation required")
