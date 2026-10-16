"""Register warehouse assets, track service dates and export JSON reports."""

import json
import tempfile
from datetime import date, datetime


class MaintenanceRegistry:
    """Keep each registry's assets and inspection interval independent."""

    def __init__(self):
        self.assets = {}
        self.service_interval_days = 90

    def register_asset(self, asset_id, machine_type, logs=None):
        """Register a unique asset; optionally append to a caller-owned log."""
        if not isinstance(asset_id, str) or not asset_id.strip():
            raise ValueError("Asset ID must be a non-empty string.")
        if not isinstance(machine_type, str) or not machine_type.strip():
            raise ValueError("Machine type must be a non-empty string.")
        asset_id = asset_id.strip()
        if asset_id in self.assets:
            raise ValueError(f"Asset {asset_id} is already registered.")
        if logs is None:
            logs = []
        self.assets[asset_id] = {
            "type": machine_type.strip(),
            "last_service": date.today().isoformat(),
        }
        logs.append(asset_id)
        print("Registered", asset_id, "- total assets:", len(self.assets))

    def update_service_date(self, asset_id, service_date):
        """Store a real, non-future date in strict YYYY-MM-DD format."""
        if asset_id not in self.assets:
            raise KeyError(f"Unknown asset: {asset_id}")
        if not isinstance(service_date, str):
            raise ValueError("Service date must use YYYY-MM-DD.")
        try:
            parsed_date = datetime.strptime(service_date, "%Y-%m-%d").date()
        except ValueError as error:
            raise ValueError("Enter a valid date using YYYY-MM-DD.") from error
        if service_date != parsed_date.isoformat():
            raise ValueError("Service date must use YYYY-MM-DD.")
        if parsed_date > date.today():
            raise ValueError("Last service date cannot be in the future.")
        self.assets[asset_id]["last_service"] = parsed_date.isoformat()

    def due_for_inspection(self):
        """Return assets serviced more than the allowed calendar days ago."""
        today = date.today()
        due = []
        for asset_id, asset in self.assets.items():
            last_service = date.fromisoformat(asset["last_service"])
            if (today - last_service).days > self.service_interval_days:
                due.append(asset_id)
        return due

    def change_interval(self, days):
        """Accept positive integer service intervals, excluding booleans."""
        if isinstance(days, bool) or not isinstance(days, int) or days <= 0:
            raise ValueError("Service interval must be a positive integer.")
        self.service_interval_days = days

    def export_service_report(self, filename="maintenance.json"):
        """Write the registry as UTF-8 JSON and always close the file."""
        with open(filename, "w", encoding="utf-8") as report:
            json.dump(self.assets, report, indent=2)
        print(f"Report written to {filename}")

    def write_scratch_copy(self):
        """Securely create a temporary JSON copy and return its saved path."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", encoding="utf-8", delete=False
        ) as scratch:
            json.dump(self.assets, scratch, indent=2)
            path = scratch.name
        print("Scratch copy at", path)
        return path

    def print_alerts(self):
        """Print an alert for every asset overdue for inspection."""
        for asset_id in self.due_for_inspection():
            print(
                "ALERT: inspection overdue for",
                asset_id,
                self.assets[asset_id]["type"],
            )


def main():
    """Run a valid demo and allow a user to enter the conveyor service date."""
    registry = MaintenanceRegistry()
    registry.register_asset("FL-01", "Forklift")
    registry.register_asset("CV-07", "Conveyor")
    registry.register_asset("PJ-03", "Pallet Jack")
    registry.update_service_date("FL-01", "2025-01-15")
    registry.change_interval(90)

    while True:
        try:
            service_date = input(
                "Last service date for CV-07 (YYYY-MM-DD, Enter to skip): "
            ).strip()
        except EOFError:
            service_date = ""
        if not service_date:
            break
        try:
            registry.update_service_date("CV-07", service_date)
        except ValueError as error:
            print(error)
        else:
            break

    if not registry.assets:
        raise RuntimeError("No assets registered.")
    registry.print_alerts()
    registry.export_service_report()
    registry.write_scratch_copy()


if __name__ == "__main__":
    main()
