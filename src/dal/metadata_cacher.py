import os
import json
import shutil


from datetime import datetime, timezone


from src.dal.category_metadata import CategoryMetadata
from src.loggers.log_utils import setup_logger


logger = setup_logger(__name__)


class MetadataCacher:


    def __init__(self) -> None:
        self.cached_metadata_dir = "./cache/category_metadata/"
        self.cached_unparsed_metadata_dir = "./cache/unparsed_category_metadata/"
        self.index_filepath = "./indices/cached_metadata.json"
        self.cached_metadata_index: dict[int, datetime] = None
        self.cached_categories: set[int] = None


    def read_cached_metadata_index(self) -> set[int]:
        with open(self.index_filepath, "r") as f:
            data = json.load(f)
            self.cached_metadata_index = {int(k): datetime.fromisoformat(v) for k, v in data.get("category_metadata", {}).items()}
            self.cached_categories = set(self.cached_metadata_index.keys())


    def cache_metadata(self, category_id: int, category_metadata: CategoryMetadata) -> None:
        metadata_dict = category_metadata.dict()
        metadata_filepath = os.path.join(self.cached_metadata_dir, f"{category_id}.json")
        
        with open(metadata_filepath, "w") as f:
            json.dump(metadata_dict, f)

        self._add_to_index(category_id)
        self._write_cached_metadata_index()


    def get_metadata(self, category_id: int) -> CategoryMetadata:
        metadata_filepath = os.path.join(self.cached_metadata_dir, f"{category_id}.json")
        
        with open(metadata_filepath, "r") as f:
            metadata_dict = json.load(f)
            metadata = CategoryMetadata(**metadata_dict)
            return metadata


    def _add_to_index(self, category_id: int) -> None:
        self.cached_metadata_index[category_id] = datetime.now(timezone.utc)
        self.cached_categories.add(category_id)


    def _write_cached_metadata_index(self) -> None:
        timestamp = datetime.now(timezone.utc).timestamp()
        backup_filepath = self.index_filepath.replace(".json", f"-{int(timestamp)}.json")
        shutil.copy(self.index_filepath, backup_filepath)

        with open(self.index_filepath, "w") as f:
            json.dump({"category_metadata": {k: v.isoformat() for k, v in self.cached_metadata_index.items()}}, f)


    def cache_unparsed_metadata(self, category_id: int, unparsed_category_metadata: str) -> None:
        unparsed_metadata_filepath = os.path.join(self.cached_unparsed_metadata_dir, f"{category_id}.txt")
        
        with open(unparsed_metadata_filepath, "w") as f:
            f.write(unparsed_category_metadata)



if __name__ == "__main__":
    os.chdir("/home/fbe/drive/projects/query_expansion")
    cacher = MetadataCacher()
    cacher.read_cached_metadata_index()
    cacher.cached_metadata_index
    cacher.cached_categories

    # cacher.add_to_index(24)
    # cacher.cached_metadata_index
    # cacher.write_cached_metadata_index()

    # cacher.read_cached_metadata_index()
    # cacher.cached_metadata_index
    # cacher.cached_categories

    with open("./outputs/category-24.json", "r") as f:
        category_metadata_json = json.load(f)
    
    category_metadata = CategoryMetadata(**category_metadata_json)
    print(category_metadata.json(indent=2))
    cacher.cache_metadata(category_id=24, category_metadata=category_metadata)
    cacher.cached_metadata_index
