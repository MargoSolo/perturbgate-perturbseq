"""Lightweight, dependency-free table schemas.

Rather than pull a heavy validation framework, each frozen table declares its
required columns, the columns that must be fully populated, and (optionally) a
controlled vocabulary for categorical columns. ``validate`` raises ``SchemaError``
with an explicit message — never a silent pass.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


class SchemaError(ValueError):
    pass


@dataclass(frozen=True)
class TableSchema:
    name: str
    required_columns: tuple[str, ...]
    non_null: tuple[str, ...] = ()
    allowed_values: dict = field(default_factory=dict)
    min_rows: int = 1

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        missing = [c for c in self.required_columns if c not in df.columns]
        if missing:
            raise SchemaError(f"[{self.name}] missing columns: {missing}")
        if len(df) < self.min_rows:
            raise SchemaError(f"[{self.name}] expected >= {self.min_rows} rows, got {len(df)}")
        for col in self.non_null:
            if df[col].isna().any():
                bad = int(df[col].isna().sum())
                raise SchemaError(f"[{self.name}] column '{col}' has {bad} null value(s)")
        for col, allowed in self.allowed_values.items():
            if col not in df.columns:
                continue
            extra = set(df[col].dropna().unique()) - set(allowed)
            if extra:
                raise SchemaError(f"[{self.name}] column '{col}' has values outside vocabulary: {sorted(extra)}")
        return df


# --- Controlled vocabularies ------------------------------------------------
FINAL_EVIDENCE_CLASSES = {
    "RETAINED_MECHANISM_HYPOTHESIS",
    "REJECTED_AFTER_DEEP_VALIDATION",
    "COMPARATOR_ONLY",
    "NOT_ADVANCED_FROM_SCREEN",
    "SAFETY_CONSTRAINED",
    "EXPLORATORY_SINGLE_STATE_HIT",
    "NONSPECIFIC_BROAD_REVERSER",
}

EVIDENCE_DEPTHS = {"SCREEN_ONLY", "SHORTLIST_VETTED", "DEEP"}

# --- Frozen table schemas ---------------------------------------------------
PRIMARY_COMPARISON = TableSchema(
    name="primary_comparison",
    required_columns=(
        "target", "final_public_label", "primary_reversal", "primary_pearson_p",
        "primary_spearman_reversal", "gsea_reversal", "guide_1_reversal", "guide_2_reversal",
        "disease_lodo_positive", "disease_lodo_total", "responder_support",
        "condition_rest", "condition_stim8", "condition_stim48",
        "matched_substrate_reversal", "matched_percentile", "matched_empirical_p",
        "matched_ci_low", "matched_ci_high", "confound_resistant", "safety_summary",
        "modality_summary", "final_decision", "principal_limitation",
    ),
    non_null=("target", "final_public_label", "primary_reversal", "final_decision"),
    min_rows=3,
)

ALL_PERTURBATIONS = TableSchema(
    name="all_perturbations_authoritative_reversal",
    required_columns=(
        "perturbation_id", "gene_symbol", "reversal_score", "global_rank", "global_percentile",
        "effect_magnitude", "breadth", "donor_sign_consistency", "guide_concordance",
        "on_target_knockdown", "broad_effect_flag", "essentiality_flag", "safety_flag",
        "modality_flag", "screen_level_status", "evidence_depth", "deep_validation_status",
        "primary_rejection_or_nonadvance_reason", "final_evidence_class", "source_artifact",
    ),
    non_null=("perturbation_id", "gene_symbol", "reversal_score", "global_rank", "evidence_depth"),
    allowed_values={"evidence_depth": EVIDENCE_DEPTHS},
    min_rows=900,
)

CANDIDATE_FUNNEL = TableSchema(
    name="candidate_funnel",
    required_columns=(
        "stage_id", "stage_name", "scope", "denominator_definition", "n_entering",
        "n_advanced", "n_not_advanced", "n_rejected", "n_unresolved",
        "principal_reason_categories", "source_artifact", "generating_command",
    ),
    non_null=("stage_id", "stage_name", "scope", "n_entering", "source_artifact"),
    min_rows=4,
)

REJECTION_LEDGER = TableSchema(
    name="rejection_ledger",
    required_columns=(
        "perturbation_id", "gene_symbol", "evidence_depth", "decision_scope",
        "last_gate_reached", "rejection_reason", "final_evidence_class",
    ),
    non_null=("perturbation_id", "gene_symbol", "evidence_depth", "final_evidence_class"),
    allowed_values={"evidence_depth": EVIDENCE_DEPTHS},
    min_rows=10,
)

GATE_MATRIX = TableSchema(
    name="gate_matrix",
    required_columns=("row_label",),
    min_rows=4,
)

MATCHED_NULL = TableSchema(
    name="matched_null",
    required_columns=("target", "observed_reversal", "empirical_p", "percentile", "n_null"),
    non_null=("target", "observed_reversal", "empirical_p"),
    min_rows=3,
)

RICTOR_ROBUSTNESS_TRACKS = TableSchema(
    name="rictor_robustness_tracks",
    required_columns=("track", "reversal", "range_low", "range_high", "source_artifact"),
    non_null=("track", "reversal", "source_artifact"),
    min_rows=11,
)

RICTOR_SERVER_SCALE_SENSITIVITIES = TableSchema(
    name="rictor_server_scale_sensitivities",
    required_columns=("track", "reversal", "source_artifact", "source_artifact_sha256",
                      "source_run_commit", "analysis_scope", "reproducibility_level"),
    non_null=("track", "reversal", "source_artifact", "source_artifact_sha256",
              "source_run_commit", "analysis_scope", "reproducibility_level"),
    min_rows=2,
)

SCHEMAS = {
    "primary_comparison": PRIMARY_COMPARISON,
    "all_perturbations_authoritative_reversal": ALL_PERTURBATIONS,
    "candidate_funnel": CANDIDATE_FUNNEL,
    "rejection_ledger": REJECTION_LEDGER,
    "gate_matrix": GATE_MATRIX,
    "matched_null": MATCHED_NULL,
    "rictor_robustness_tracks": RICTOR_ROBUSTNESS_TRACKS,
    "rictor_server_scale_sensitivities": RICTOR_SERVER_SCALE_SENSITIVITIES,
}
