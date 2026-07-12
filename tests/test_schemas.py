"""Schema validation accepts the frozen tables and rejects malformed ones."""
import pandas as pd
import pytest

from perturbgate.io import frozen_dir
from perturbgate.schemas import SCHEMAS, SchemaError, TableSchema


@pytest.mark.parametrize("name", list(SCHEMAS))
def test_frozen_tables_pass_their_schema(name):
    df = pd.read_csv(frozen_dir() / f"{name}.tsv", sep="\t")
    SCHEMAS[name].validate(df)  # must not raise


def test_missing_column_raises():
    s = TableSchema("t", required_columns=("a", "b"))
    with pytest.raises(SchemaError, match="missing columns"):
        s.validate(pd.DataFrame({"a": [1]}))


def test_null_in_required_column_raises():
    s = TableSchema("t", required_columns=("a",), non_null=("a",))
    with pytest.raises(SchemaError, match="null"):
        s.validate(pd.DataFrame({"a": [1, None]}))


def test_vocabulary_violation_raises():
    s = TableSchema("t", required_columns=("x",), allowed_values={"x": {"A", "B"}})
    with pytest.raises(SchemaError, match="vocabulary"):
        s.validate(pd.DataFrame({"x": ["A", "C"]}))
