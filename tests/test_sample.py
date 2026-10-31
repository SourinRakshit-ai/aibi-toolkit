from aibi_toolkit.sample import sample_model, sample_csv


def test_sample_model_deterministic():
    a = sample_model(seed=7)
    b = sample_model(seed=7)
    assert a == b


def test_sample_model_shape():
    m = sample_model(tables=3, measures_per_table=2)
    assert len(m["tables"]) == 3
    assert len(m["relationships"]) == 2


def test_sample_csv(tmp_path):
    p = tmp_path / "s.csv"
    assert sample_csv(p, rows=5) == 5
