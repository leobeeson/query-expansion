import pandas as pd


from src.dal.query_set import QuerySet


class DataLoader:
    

    def __init__(self, category_id: int, data_path: str ="./data/trainSet.csv", num_samples: int = 400, seed: int = 235) -> None:
        self.data_path = data_path
        self.category_id = category_id
        self.num_samples = num_samples
        self.seed = seed


    def get_category_queries(self) -> QuerySet:
        category_queries = self._load_data()
        category_query_set = QuerySet(category_id=self.category_id, queries=category_queries)
        return category_query_set
    
    
    def _load_data(self) -> list[str]:
        data = pd.read_csv(self.data_path, header=None, names=["query", "category"])
        filtered_data = data[data["category"] == self.category_id]
        sampled_queries = filtered_data["query"].sample(n=min(self.num_samples, len(filtered_data)), random_state=self.seed)
        return sampled_queries.tolist()


if __name__ == "__main__":
    data_loader = DataLoader(data_path="./data/trainSet.csv", category_id=24)
    query_set: QuerySet = data_loader.get_category_queries()
    print(query_set.json(indent=2))