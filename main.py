from dotenv import load_dotenv, find_dotenv


from src.app_controllers.metadata_generator import MetadataGenerator
from src.loggers.log_utils import setup_logger


_ = load_dotenv(find_dotenv())


# logger = setup_logger("")


def main():
    categories = set(range(0, 1420))
    metadata_generator = MetadataGenerator(categories=categories)
    # metadata_generator.get_category_taxonomies()
    metadata_generator.get_query_audits()


if __name__ == "__main__":
    main()
