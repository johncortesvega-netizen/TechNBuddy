# Patch TB-01 Recovery Note

If this patch causes issues, revert these changes:

1. Remove the vendored `sydney_protocol_core/` directory.
2. Restore the previous `app.py`, `README.md`, and `requirements.txt`.
3. Remove `PATCH_STATUS.md`, `PATCH_TB_01_MANIFEST.txt`, `PATCH_TB_01_RECOVERY_NOTE.md`, and `tests/test_tb_01_core_connection.py` if they were only introduced by this patch.

This patch intentionally avoids changing the app into a multi-module interface. If the UI shows module cards or scores, that is outside TB-01 scope and should be reverted.
