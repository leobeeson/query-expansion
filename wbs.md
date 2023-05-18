# Work Breakdown Structure

## Project Definition

An application that can:

1. Cluster a set of related search queries into a coherent product/market `category` (henceforth ``category``).
2. Qualitatively describe `categories`, its potential `subcategories`, and most representative `products`, `services`, `brands`, and `companies`.
3. Given a search query, decide to which `categories` it is most relevant, and why.
4. Given a search query, suggest other related `categories` it could be associated to, and why.
5. Given a set of labelled search queries, identify search queries that are potentially misclassified, suggest a more relevant `category`, and why.

## Deliverables

1. API POST endpoint that receives a batch of search queries, and returns its `category` metadata.
2. API GET endpoint that receives a `category`'s label or id, and returns its metadata.
3. API GET endpoint that receives a search query string, and returns its most relevant `category`.
4. API GET endpoint that receives a search query string, and returns its top-n most relevant associated `categories`.
5. API POST endpoint that receives a batch of labelled search queries, and returns for every search query:
   * A `relevance` score for its current `category` label.
   * A suggested label for its most relevant `category`.
   * A `relevance` score for the suggested most relevant `category`.

## Tasks

### Generate Category Metadata

* For a given set of search queries:
  * Generate a **`category` label**.
  * Generate a set of **`subcategory` labels**, and corresponding relevance score towards the `category`.
  * Generate a set of **key `nouns`**, and corresponding relevance score towards the `category`.
  * Generate a set of **products, services, brands, and companies**, and corresponding relevance score towards the `category`.
  * Persist `category` metadata, and the set of search queries used to generate it.

## Work Packages

* Generate Category Metadata:
  * Create DTO for set of search queries associated to a same category.
  * Create Output Parser Schemas for labels and relevance scores for `category`, `subcategory`, `nouns`, `products`, `services`, `brands`, and `companies`.
  * Create Prompt Template for sending search queries, and response schema.
  * Create response parser.
  * Create persistance layer for `category` metadata.
  * Create DAL for `category` metadata.
