import os
from datetime import datetime
from pathlib import Path

import pytest

from cipug.service import Service
from cipug.tools.snapshot import Snapper


def test_snapper_real():
    service_path = Path("/tmp/btrfs_mount")
    assert service_path.exists(), (
        "BTRFS dummy mount not found. Please ensure the test environment "
        "is correctly configured."
    )
    os.environ["CIPUG_SERVICES_ROOT"] = "/tmp"
    os.environ["CIPUG_SNAPSHOTS_DIR_SNAPPER"] = ".snapshots"

    snapper = Snapper()
    # We should have the 'envconf' config we set up in CI
    assert any(c["config"] == "envconf" for c in snapper.configs)
    service = Service(service_path)
    # We now simulate snapshotting a folder
    t_before_snapshot = datetime.now()
    snapper.create_snapshot(service, "testmessage")
    t_after_snapshot = datetime.now()
    # Test if retrieving the snapshot datetime works correctly
    t_snapshot: datetime | None = snapper.get_last_snapshot_date(service)
    assert t_snapshot is not None
    # The BTRFS info.xml timestamp might differ slightly from python's datetime.now()
    assert t_before_snapshot.timestamp() - 5 <= t_snapshot.timestamp() <= t_after_snapshot.timestamp() + 5

    # Simulate snapshotting something that doesn't exist
    with pytest.raises(Exception):
        snapper.create_snapshot(Service(Path("/this/does/not/exist")), "testmessage")
