import os
from datetime import datetime
from pathlib import Path

import pytest

from cipug.service import Service
from cipug.tools.snapshot.zfs import Zfs


def test_zfs_snapshot_real():
    os.environ["CIPUG_SERVICES_ROOT"] = "/testpool"
    service_path = Path("/testpool")
    assert service_path.exists(), (
        "ZFS dummy pool not found. Please ensure the test environment "
        "is correctly configured."
    )

    tool = Zfs()
    tool.assert_dependencies()

    service = Service(service_path)

    t_before = datetime.now()
    tool.create_snapshot(service, "test message")
    t_after = datetime.now()

    # Test get_last_snapshot_date
    last_date = tool.get_last_snapshot_date(service)
    assert last_date is not None
    assert t_before.timestamp() - 5 <= last_date.timestamp() <= t_after.timestamp() + 5

    # Test snapshot with image hash
    image_hash = "1234567890abcdef1234567890abcdef"
    tool.create_snapshot(service, "test message", image_hash=image_hash)

    # Test failure: Path does not exist
    with pytest.raises(Exception) as excinfo:
         tool.create_snapshot(Service(Path("/non/existent/path")), "msg")
    assert "does not exist" in str(excinfo.value)

    # Test failure: not a ZFS mount
    error_path = Path("/tmp/not_a_zfs_mount")
    error_path.mkdir(exist_ok=True)
    with pytest.raises(Exception) as excinfo:
        tool.create_snapshot(Service(error_path), "msg")
    assert "Could not determine ZFS dataset" in str(excinfo.value)
