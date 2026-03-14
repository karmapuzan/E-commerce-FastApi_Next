from src.core.auth import RoleChecker


admin_vendor_only = RoleChecker(allowed_roles=["ADMIN", "VENDOR"])
