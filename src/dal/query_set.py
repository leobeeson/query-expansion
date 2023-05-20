from pydantic import BaseModel, Field


from src.dal.category_metadata import CategoryMetadata


class QuerySet(BaseModel):

    category_id: int = Field(description="Unique identifier for a market category.")
    queries: list[str] = Field(description="A set of user search queries that are relevant to a market category.", default_factory=list)
    category_metadata: CategoryMetadata = Field(description="Metadata about the market category that the queries are relevant to.", default=None)


    def add_query(self, query: str) -> None:
        self.queries.append(query)


    def add_queries(self, queries: list[str]) -> None:
        self.queries.extend(queries)
    
    
    def get_queries(self) -> list[str]:
        return self.queries
    
