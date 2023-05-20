import json
import shutil


from datetime import datetime, timezone


from src.dal.category_metadata import CategoryMetadata


class MetadataCacher:


    def __init__(self) -> None:
        self.cached_metadata_dir = "./cache/category_metadata/"
        self.index_filepath = "./indices/cached_metadata.json"
        self.cached_metadata_index: dict[int, datetime] = None
        self.cached_categories: set[int] = None


    def read_cached_metadata_index(self) -> set[int]:
        with open(self.index_filepath, "r") as f:
            data = json.load(f)
            self.cached_metadata_index = {int(k): datetime.fromisoformat(v) for k, v in data.get("category_metadata", {}).items()}
            self.cached_categories = set(self.cached_metadata_index.keys())


    def add_to_index(self, category_id: int) -> None:
        self.cached_metadata_index[category_id] = datetime.now(timezone.utc)
        self.cached_categories.add(category_id)


    def write_cached_metadata_index(self) -> None:
        # Create a copy of the current index file for version control
        timestamp = datetime.now(timezone.utc).timestamp()
        backup_filepath = self.index_filepath.replace(".json", f"-{int(timestamp)}.json")
        shutil.copy(self.index_filepath, backup_filepath)

        # Write the updated index to the index file
        with open(self.index_filepath, "w") as f:
            json.dump({"category_metadata": {k: v.isoformat() for k, v in self.cached_metadata_index.items()}}, f)


    def cache_metadata(self, category_metadata: CategoryMetadata) -> None:
        pass


if __name__ == "__main__":
    cacher = MetadataCacher()
    cacher.read_cached_metadata_index()
    cacher.cached_metadata_index
    cacher.cached_categories

    cacher.add_to_index(24)
    cacher.cached_metadata_index
    cacher.write_cached_metadata_index()

    cacher.read_cached_metadata_index()
    cacher.cached_metadata_index
    cacher.cached_categories
