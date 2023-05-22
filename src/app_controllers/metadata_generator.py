import time
from tqdm import tqdm


from src.dal.metadata_cacher import MetadataCacher
from src.dal.data_loader import DataLoader
from src.dal.query_set import QuerySet
from src.client_layer.llm_client import LLMCLient
from src.dal.category_metadata import CategoryMetadata
from src.dal.audit_cacher import AuditCacher
from src.dal.category_audit import CategoryAudit
from src.loggers.log_utils import setup_tqdm_logger


class MetadataGenerator:

    
    def __init__(self, categories: set[int]) -> None:
        self.logger = setup_tqdm_logger(__name__)
        self.metadata_cacher = MetadataCacher()
        self.audit_cacher = AuditCacher()
        self.llm_client = LLMCLient()
        self.categories = categories


    def get_categories_to_process(self) -> set[int]:
        self.metadata_cacher.read_cached_metadata_index()
        unprocessed_categories: set[int] = self.categories - self.metadata_cacher.cached_categories
        return unprocessed_categories
    

    def get_categories_to_audit(self) -> set[int]:
        self.audit_cacher.read_cached_metadata_index()
        unprocessed_categories: set[int] = self.categories - self.audit_cacher.cached_categories
        return unprocessed_categories

    
    def compact_search_queries(self, search_queries: list[str]) -> str:
        search_queries_compact = "; ".join(search_queries)
        return search_queries_compact


    def get_category_taxonomies(self) -> None:
        unprocessed_categories = self.get_categories_to_process()
        self.logger.info(f"Number of categories to process: {len(unprocessed_categories)}")
        processed_categories = 0
        for category_id in tqdm(unprocessed_categories):
            time.sleep(1)
            self.logger.info(f"Total categories to go: {len(unprocessed_categories) - processed_categories}")
            processed_categories += 1
            self.logger.info(f"PROCESSING CATEGORY: {category_id}")
            data_loader = DataLoader(category_id=category_id)
            query_set: QuerySet = data_loader.get_category_queries()
            search_queries_compact: str = self.compact_search_queries(query_set.get_queries())
            try:
                t0 = time.time()
                response: CategoryMetadata = self.llm_client.generate_taxonomy(search_queries_compact)
                t1 = time.time()
                self.logger.info(f"LLM response time for category {category_id}: {t1 - t0}")
                try:
                    parsed_response = self.llm_client.parser.parse(response)
                    t2 = time.time()
                    self.metadata_cacher.cache_metadata(category_id=category_id, category_metadata=parsed_response)
                    self.logger.info(f"Time with parsing for category {category_id}: {t2 - t0}")
                except Exception as e:
                    self.logger.error(f"Error parsing response for category {category_id}:\n{type(e).__name__}")
                    try:
                        parsed_response = self.llm_client.fix_parsing(response)
                        t3 = time.time()
                        self.metadata_cacher.cache_metadata(category_id=category_id, category_metadata=parsed_response)
                        self.logger.info(f"Time with fix parsing for category {category_id}: {t3 - t0}")
                    except Exception as e:
                        self.logger.error(f"Error fixing parsing for category {category_id}:\n{type(e).__name__}")
                        self.metadata_cacher.cache_unparsed_metadata(category_id=category_id, unparsed_category_metadata=response)
                        t4 = time.time()
                        self.logger.info(f"Unparsed metadata for category {category_id} cached.")
                        self.logger.info(f"Time with failed parsing for category {category_id}: {t4 - t0}")
                        continue
                    continue
            except Exception as e:
                self.logger.error(f"Error generating taxonomy for category {category_id}:\n{type(e).__name__}")
                continue 


    def get_query_audits(self) -> None:
        unprocessed_categories = self.get_categories_to_audit()
        self.logger.info(f"Number of categories to process: {len(unprocessed_categories)}")
        processed_categories = 0
        for category_id in tqdm(unprocessed_categories):
            time.sleep(1)
            self.logger.info(f"Total categories to go: {len(unprocessed_categories) - processed_categories}")
            processed_categories += 1
            self.logger.info(f"PROCESSING CATEGORY: {category_id}")
            data_loader = DataLoader(category_id=category_id, num_samples=100)
            query_set: QuerySet = data_loader.get_category_queries()
            category_taxonomy: CategoryMetadata = self.metadata_cacher.get_metadata(category_id=category_id)
            category_taxonomy_compact: str = f"{category_taxonomy.dict()}"
            try:
                t0 = time.time()
                response: str = self.llm_client.audit_queries(category_taxonomy=category_taxonomy_compact, search_queries=query_set.get_queries())
                t1 = time.time()
                self.logger.info(f"LLM response time for category {category_id}: {t1 - t0}")
                try:
                    parsed_response: CategoryAudit = self.llm_client.parser_audit.parse(response)
                    t2 = time.time()
                    self.audit_cacher.cache_audit(category_id=category_id, category_audit=parsed_response)
                    self.logger.info(f"Time with parsing for category {category_id}: {t2 - t0}")
                except Exception as e:
                    self.logger.error(f"Error parsing response for category {category_id}:\n{type(e).__name__}")
                    try:
                        parsed_response: CategoryAudit = self.llm_client.fix_parsing_audit(response)
                        t3 = time.time()
                        self.audit_cacher.cache_audit(category_id=category_id, category_audit=parsed_response)
                        self.logger.info(f"Time with fix parsing for category {category_id}: {t3 - t0}")
                    except Exception as e:
                        self.logger.error(f"Error fixing parsing for category {category_id}:\n{type(e).__name__}")
                        self.audit_cacher.cache_unparsed_audit(category_id=category_id, unparsed_category_audit=response)
                        t4 = time.time()
                        self.logger.info(f"Unparsed metadata for category {category_id} cached.")
                        self.logger.info(f"Time with failed parsing for category {category_id}: {t4 - t0}")
                        continue
                    continue
            except Exception as e:
                self.logger.error(f"Error generating taxonomy for category {category_id}:\n{type(e).__name__}")
                continue 
