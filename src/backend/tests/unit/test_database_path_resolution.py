"""Tests for database path resolution in settings.

These tests verify that the database path is correctly resolved
based on the save_db_in_config_dir setting and primeagent package availability.
"""

import os
from pathlib import Path
from unittest.mock import patch


class TestDatabasePathResolution:
    """Test database path resolution in Settings."""

    def test_database_path_uses_primeagent_package_when_save_db_in_config_dir_false(self, tmp_path):
        """When save_db_in_config_dir=False, database should be in primeagent package dir."""
        import primeagent
        from wfx.services.settings.base import Settings

        env_vars = {
            "PRIMEAGENT_CONFIG_DIR": str(tmp_path),
            "PRIMEAGENT_SAVE_DB_IN_CONFIG_DIR": "false",
        }
        # Remove DATABASE_URL from env to trigger path resolution
        env = {k: v for k, v in os.environ.items() if k != "PRIMEAGENT_DATABASE_URL"}
        env.update(env_vars)

        with patch.dict(os.environ, env, clear=True):
            settings = Settings()

        expected_dir = Path(primeagent.__file__).parent.resolve()
        assert settings.database_url is not None
        # The database_url should contain the primeagent package path
        assert str(expected_dir) in settings.database_url

    def test_database_path_uses_config_dir_when_save_db_in_config_dir_true(self, tmp_path):
        """When save_db_in_config_dir=True, database should be in config_dir."""
        from wfx.services.settings.base import Settings

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        env_vars = {
            "PRIMEAGENT_CONFIG_DIR": str(config_dir),
            "PRIMEAGENT_SAVE_DB_IN_CONFIG_DIR": "true",
        }
        # Remove DATABASE_URL from env to trigger path resolution
        env = {k: v for k, v in os.environ.items() if k != "PRIMEAGENT_DATABASE_URL"}
        env.update(env_vars)

        with patch.dict(os.environ, env, clear=True):
            settings = Settings()

        assert settings.database_url is not None
        assert str(config_dir) in settings.database_url

    def test_database_path_falls_back_to_wfx_when_primeagent_not_importable(self, tmp_path):
        """When primeagent is not importable, should fall back to wfx package path."""
        import builtins

        import wfx.services.settings.base as settings_module
        from wfx.services.settings.base import Settings

        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "primeagent":
                raise ImportError(name)
            return original_import(name, *args, **kwargs)

        env_vars = {
            "PRIMEAGENT_CONFIG_DIR": str(tmp_path),
            "PRIMEAGENT_SAVE_DB_IN_CONFIG_DIR": "false",
        }
        env = {k: v for k, v in os.environ.items() if k != "PRIMEAGENT_DATABASE_URL"}
        env.update(env_vars)

        with (
            patch.dict(os.environ, env, clear=True),
            patch.object(builtins, "__import__", side_effect=mock_import),
        ):
            settings = Settings()

        # Should fall back to wfx path
        wfx_path = Path(settings_module.__file__).parent.parent.parent.resolve()
        assert settings.database_url is not None
        assert str(wfx_path) in settings.database_url

    def test_explicit_database_url_env_var_takes_precedence(self, tmp_path):
        """PRIMEAGENT_DATABASE_URL env var should take precedence over path resolution."""
        from wfx.services.settings.base import Settings

        custom_url = "sqlite:///custom/path/test.db"

        with patch.dict(
            os.environ,
            {"PRIMEAGENT_DATABASE_URL": custom_url, "PRIMEAGENT_CONFIG_DIR": str(tmp_path)},
            clear=False,
        ):
            settings = Settings(config_dir=str(tmp_path))

        assert settings.database_url == custom_url
