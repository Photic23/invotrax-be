from rolepermissions.roles import AbstractUserRole

class customer(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
        'manage_staff': True,
        'system_settings': True,
        'staff_permission': True,
    }

class vendor(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
        'manage_staff': True,
        'system_settings': True,
        'staff_permission': True,
    }

class staff(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
        'manage_staff': True,
        'system_settings': True,
        'staff_permission': True,
    }

class manager(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
        'manage_staff': True,
        'system_settings': True,
        'staff_permission': True,
        'manage_kontrak': True, # Manajemen Kontrak devin
    }

class admin(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
        'manage_staff': True,
        'system_settings': True,
        'staff_permission': True,
    }

class Owner(AbstractUserRole):
    """
    Owner role with all permissions from Staff, Manager, and Admin roles combined
    """
    available_permissions = {
        # From Staff role
        'view_own_profile': True,
        'edit_own_profile': True,
        'view_pengajuan': True,
        'process_pengajuan': True,
        'view_users': True,
        'manage_basic_data': True,
        
        # From Manager role (includes all Staff permissions plus these)
        'approve_pengajuan': True,
        'manage_users': True,
        'view_reports': True,
        'manage_vendors': True,
        
        # From Admin role (includes all Manager permissions plus these)
        'delete_users': True,
        'system_configuration': True,
        'manage_roles': True,
    }