from pathlib import Path

from enterprise_lakehouse.common.metadata import (
    YamlMetadataRepository,
)


def test_load_yaml_metadata(
    tmp_path: Path,
) -> None:

    yaml_file = tmp_path / "sources.yaml"

    yaml_file.write_text(
        """
sources:

  - source_id: orders

    source_system: sales

    source_type: file

    load_type: full

    file_format: json

    location:

      object_name: orders

      path: /landing/orders

    target:

      catalog_name: dev_sales_lakehouse

      bronze_table: bronze_orders

    governance:

      business_domain: sales

      owner: platform
""",
        encoding="utf-8",
    )

    repository = YamlMetadataRepository(yaml_file)

    metadata = repository.load()

    assert len(metadata) == 1

    assert metadata[0].source_id == "orders"

    assert metadata[0].target.catalog_name == "dev_sales_lakehouse"
