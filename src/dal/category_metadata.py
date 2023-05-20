from pydantic import BaseModel, Field
from enum import Enum


class EntityType(str, Enum):
    PRODUCT = "product"
    SERVICE = "service"
    BRAND = "brand"
    COMPANY = "company"
    OTHER = "other"


class Subcategory(BaseModel):

    label: str = Field(
        description="Short phrase that best reifies the market subcategory encompassed by a subset of user search queries.",
        example="Bubble Wrap and Padded Envelopes"
        )
    relevance: float = Field(description="Number between 0 and 1 indicating how relevant the subcategory is to the overall market category. For example, if the market category is 'Postal and Packaging Supplies', the subcategory 'Cardboard Tubes' is highly relevant, while the subcategory 'Toothpaste Tubes' is less so.")
    description: str = Field(description="One sentence describing the subcategory.")
    nouns: list[str] = Field(description="Noun phrases present in the subcategory that represent real tangible things.")
    subtopics: list[str] = Field(description="Short phrases that reify subcategories of the subcategory.")


class CategoryMetadata(BaseModel):
    
    label: str = Field(
        description="Short phrase that best reifies the market category encompassed by a set of user search queries. Maixmum five words Long.",
        example="Postal and Packaging Supplies"
        )
    description: str = Field(description="One sentence that describes the market category and subcategories.")
    intents: list[str] = Field(
        description="Short phrases describing users' most relevant intents when using these types of search queries, i.e. what problem or need they are trying to solve. Maximum ten intents.",
        example="Ship furniture when moving to a new home."
        )
    entities: list[str] = Field(description="Short phrases describing products, services, brands, and company names most relevant among user search queries in this category.")
    subcategories: list[Subcategory] = Field(description="Most relevant subcategories that best clusters search queries for this market category. Sorted from most relevant to least relevant. Maximum ten subcategories.")


if __name__ == "__main__":
    from langchain.output_parsers import PydanticOutputParser

    parser = PydanticOutputParser(pydantic_object=CategoryMetadata)
    print(parser.get_format_instructions())


