from pydantic import BaseModel, Field


class QueryAudit(BaseModel):

    query: str = Field(description="The exact search query without any changes.")
    relevance: float = Field(description="Number between 0 and 1 indicating how relevant the query is to the market category.")


class CategoryAudit(BaseModel):

    query_audits: list[QueryAudit] = Field(description="A set of user search queries and their corresponding relevance to the market category.", default_factory=list)
