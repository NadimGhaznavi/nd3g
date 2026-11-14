from typing import Final


class DNd3G:
    VERSION: Final[str] = "0.3.0"
    CMDB_TYPE: Final[str] = "application"
    CMDB_SUBTYPE: Final[str] = "Application"
    CMDB_SUPPLIER: Final[str] = "Nadim-Daniel"
    CMDB_CODENAME: Final[str] = "Mut"
    CMDB_COMPONENTS = ()
    CMDB_DATABASES = ()
    # Declare every owned listener; runtime defaults must use these bindings.
    CMDB_NETWORK: Final[tuple[tuple[str, str, int], ...]] = ()
    BASE_DIR: Final[str] = "/opt/prod/nd3g"
