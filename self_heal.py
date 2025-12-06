# self_heal.py
#!/usr/bin/env python3
import threading
import logging
import time
import json
import sqlite3
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("ntrli.health")

class HealthMonitor:
    def __init__(self):
        self.running = False
        self.errors = []
        self.restarts = 0
        self.last_heartbeat = datetime.now()
        self.data_dir = Path(__file__).parent / "data"
        self.health_file = self.data_dir / "health.json"
        self.db_path = Path(__file__).parent / "ntrli_superbot.db"
        self.data_dir.mkdir(exist_ok=True)
        (Path(__file__).parent / "logs").mkdir(exist_ok=True)

    def start(self):
        self.running = True
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()
        logger.info("HealthMonitor started")

    def stop(self):
        self.running = False
        logger.info("HealthMonitor stopped")

    def _loop(self):
        while self.running:
            try:
                self.heartbeat()
                self.check_db()
                self.check_files()
                time.sleep(60)
            except Exception as e:
                logger.error(f"HealthMonitor error: {e}")
                self._log_error(str(e))

    def heartbeat(self):
        self.last_heartbeat = datetime.now()
        health = {
            "timestamp": self.last_heartbeat.isoformat(),
            "restarts": self.restarts,
            "errors": len(self.errors)
        }
        try:
            with open(self.health_file, "w") as f:
                json.dump(health, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not write health file: {e}")

    def check_db(self):
        if not self.db_path.exists():
            logger.warning("DB missing")
            return
        try:
            conn = sqlite3.connect(str(self.db_path), timeout=5)
            cur = conn.cursor()
            cur.execute("PRAGMA integrity_check")
            row = cur.fetchone()
            if row and row[0] != "ok":
                logger.warning(f"DB integrity: {row}")
                self._repair_db()
            conn.close()
        except Exception as e:
            logger.error(f"DB check failed: {e}")
            self._repair_db()

    def _repair_db(self):
        try:
            backup_dir = self.data_dir / ".backups"
            backup_dir.mkdir(exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup = backup_dir / f"ntrli_db_{ts}.bak"
            if self.db_path.exists():
                with open(self.db_path, "rb") as src, open(backup, "wb") as dst:
                    dst.write(src.read())
                logger.info(f"DB backup created: {backup}")
            # try PRAGMA optimize as light repair
            conn = sqlite3.connect(str(self.db_path))
            conn.execute("PRAGMA optimize")
            conn.commit()
            conn.close()
            logger.info("DB optimize attempted")
        except Exception as e:
            logger.error(f"DB repair failed: {e}")

    def check_files(self):
        # simple checks for data json files (if present)
        for f in ["data/bot_data.json", "data/users.json"]:
            p = Path(__file__).parent / f
            if p.exists():
                try:
                    with open(p, "r") as fh:
                        json.load(fh)
                except Exception as e:
                    logger.warning(f"Data file corrupted: {p}, error: {e}")
                    self._repair_file(p)

    def _repair_file(self, p: Path):
        try:
            backup_dir = self.data_dir / ".backups"
            backup_dir.mkdir(exist_ok=True)
            b = backup_dir / f"{p.name}.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            p.rename(b)
            default = {} if p.name == "bot_data.json" else {}
            with open(p, "w") as fh:
                json.dump(default, fh)
            logger.info(f"Repaired file {p}")
        except Exception as e:
            logger.error(f"Repair file failed: {e}")

    def _log_error(self, msg: str):
        self.errors.append({"ts": datetime.now().isoformat(), "msg": msg})
        if len(self.errors) > 200:
            self.errors = self.errors[-200:]

# global monitor
_monitor = None
def get_monitor():
    global _monitor
    if _monitor is None:
        _monitor = HealthMonitor()
    return _monitor
