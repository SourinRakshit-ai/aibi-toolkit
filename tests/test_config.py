from aibi_toolkit.config import load_config, validate_config


def test_defaults(tmp_path):
    cfg = load_config(tmp_path / "missing.toml")
    assert cfg["default_currency"] == "USD"


def test_validate_ok():
    assert validate_config(load_config("/nonexistent")) == []


def test_validate_bad():
    assert validate_config({"max_name_length": -1})


def test_fallback_parser():
    from aibi_toolkit.config import _parse_simple_toml
    data = _parse_simple_toml('[aibi]\nmax_name_length = 32  # inline comment\nflag = true\nname = "x"\n')
    assert data["aibi"]["max_name_length"] == 32
    assert data["aibi"]["flag"] is True
    assert data["aibi"]["name"] == "x"


def test_load_config_without_tomllib(tmp_path, monkeypatch):
    from aibi_toolkit import config
    monkeypatch.setattr(config, "tomllib", None)
    p = tmp_path / "aibi.toml"
    p.write_text('[aibi]\nmax_name_length = 32\n', encoding="utf-8")
    assert config.load_config(p)["max_name_length"] == 32


def test_starter_toml():
    from aibi_toolkit.config import default_config_toml
    assert "[aibi]" in default_config_toml()
