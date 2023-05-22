import os
import json
import shutil


from datetime import datetime, timezone


from src.dal.category_audit import CategoryAudit
from src.loggers.log_utils import setup_logger


logger = setup_logger(__name__)


class AuditCacher:


    def __init__(self) -> None:
        self.cached_audit_dir = "./cache/audit_label/"
        self.cached_unparsed_audit_dir = "./cache/unparsed_audit_label/"
        self.index_filepath = "./indices/cached_audits.json"
        self.cached_audits_index: dict[int, datetime] = None
        self.cached_categories: set[int] = None


    def read_cached_metadata_index(self) -> set[int]:
        with open(self.index_filepath, "r") as f:
            data = json.load(f)
            self.cached_audits_index = {int(k): datetime.fromisoformat(v) for k, v in data.get("query_label", {}).items()}
            self.cached_categories = set(self.cached_audits_index.keys())


    def cache_audit(self, category_id: int, category_audit: CategoryAudit) -> None:
        audit_dict = category_audit.dict()
        audit_filepath = os.path.join(self.cached_audit_dir, f"{category_id}.json")
        
        with open(audit_filepath, "w") as f:
            json.dump(audit_dict, f)

        self._add_to_index(category_id)
        self._write_cached_audit_index()


    def get_metadata(self, category_id: int) -> CategoryAudit:
        audit_filepath = os.path.join(self.cached_audit_dir, f"{category_id}.json")
        
        with open(audit_filepath, "r") as f:
            audit_dict = json.load(f)
            audit = CategoryAudit(**audit_dict)
            return audit


    def _add_to_index(self, category_id: int) -> None:
        self.cached_audits_index[category_id] = datetime.now(timezone.utc)
        self.cached_categories.add(category_id)


    def _write_cached_audit_index(self) -> None:
        timestamp = datetime.now(timezone.utc).timestamp()
        backup_filepath = self.index_filepath.replace(".json", f"-{int(timestamp)}.json")
        shutil.copy(self.index_filepath, backup_filepath)

        with open(self.index_filepath, "w") as f:
            json.dump({"query_label": {k: v.isoformat() for k, v in self.cached_audits_index.items()}}, f)


    def cache_unparsed_audit(self, category_id: int, unparsed_category_audit: str) -> None:
        unparsed_audit_filepath = os.path.join(self.cached_unparsed_audit_dir, f"{category_id}.txt")
        
        with open(unparsed_audit_filepath, "w") as f:
            f.write(unparsed_category_audit)



if __name__ == "__main__":
    pass
