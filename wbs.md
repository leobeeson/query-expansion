# Work Breakdown Structure

## Project Definition

An application that can:

1. Cluster a set of related search queries into a coherent product/market `category` (henceforth `category`).
2. Qualitatively describe `categories`, its potential `subcategories`, and most representative `products`, `services`, `brands`, and `companies`.
3. Given a search query, decide to which `categories` it is most relevant, and why.
4. Given a search query, suggest other related `categories` it could be associated to, and why.
5. Given a set of labelled search queries, identify search queries that are potentially misclassified, suggest a more relevant `category`, and why.
   * Use to **retrain transformer model**.
6. Given a small set of search queries from an unbalanced class, suggest similar search queries for upsampling category, and balancing training set.
   * Use to **retrain transformer model**.

## Deliverables

1. API POST endpoint that receives a batch of search queries, and returns its `category` metadata.
2. API GET endpoint that receives a `category`'s id, and returns its metadata.
3. API GET endpoint that receives a search query string, and returns its most relevant `category`.
4. API GET endpoint that receives a search query string, and returns its top-n most relevant associated `categories`.
5. API POST endpoint that receives a batch of labelled search queries, and returns for every search query:
   * A `relevance` score for its current `category` label.
   * A suggested label for its most relevant `category`.
   * A `relevance` score for the suggested most relevant `category`.
6. API POST endpoint that receives a batch of search queries belonging to the same `category`, and returns similar search queries.

## Tasks

### Generate Category Metadata

* For a given set of search queries:
  * Generate a **`category` label**.
  * Generate a set of **`subcategory` labels**, and corresponding relevance score towards the `category`.
  * Generate a set of **key `entities`**, and corresponding relevance score towards the `category`.
  * Generate a set of **products, services, brands, and companies**, and corresponding relevance score towards the `category`.
  * Persist `category` metadata, and the set of search queries used to generate it.

### Identify a Search Query's Most Relevant Category

* For a given search query:
  * Retrieve it's `category` and `category` metadata from db/cache, if present.
  * Given a user flag, query the LLM to predict its most relevant category.
  * Given an additional user flag, query the LLM, but first query Google, pass SERP's product results to LLM, and predict its most relevant category.
  * Store the LLM category prediction in cache.
  * Allow user to decide if updating the search query's previous persisted prediction with current prediction.

### Improve Model Training Data

#### Option 1: OpenAI API

* For every category:
  * Provide the LLM with its metadata.
  * Provide the LLM with its batch of search queries
  * Make the LLM assign a relevance score to very search query.
  * Rank the search queries by relevance score.
  * Identify a threshold for chosing search queries to re-valuate their category.
* For every search query under the threshold:
  * Ask the model to suggest the user's intent.
  * Compare it to every category's embedded (with the same fine-tuned model) metadata.
  * Define thresholds of certainty/uncertainty to select search queries that require reclassification.
  * Replace category_id assigned to it in training data with most likely from cosine similarity.

#### Option 2: Fine-Tuned Causal Generation Model

* For every search query:
  * Ask the LLM to infer the user's intent.
  * Embed it's answer with the fine-tuned model.
  * Compare it to every category's embedded (with the same fine-tuned model) metadata.
  * Define thresholds of certainty/uncertainty to select search queries that require reclassification.
  * Replace category_id assigned to it in training data with most likely from cosine similarity.

## Work Packages

* Generate Category Metadata:
  * Create DTO for set of search queries associated to a same category. #DONE
  * Create Output Parser Schemas for labels and relevance scores for `category`, `subcategory`, `entities`, `products`, `services`, `brands`, and `companies`. #DONE
  * Create Prompt Template for sending search queries, and response schema. #DONE
  * Create response parser. #DONE
  * Create DataLoader class for loading raw search queries into a DTO. #DONE
  * Create persistance layer for `category` metadata. #DONE
  * Create index for tracking categories with and without metadata. #DONE
  * Create QueryHandler for calling LLM, store results, and update index for success or failure of call. #FOCUS
  * Create DAL for `category` metadata.
