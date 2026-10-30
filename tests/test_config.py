from aibi_toolkit.config import load_config, validate_config


def test_defaults(tmp_path):
    cfg = load_config(tmp_path / "missing.toml")
    assert cfg["default_currency"] == "USD"


def test_validate_ok():
    assert validate_config(load_config("/nonexistent")) == []


def test_validate_bad():
    assert validate_config({"max_name_length": -1})


def test_starter_toml():
    from aibi_toolkit.config import default_config_toml
    assert "[aibi]" in default_config_toml()
