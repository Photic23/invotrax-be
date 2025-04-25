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
        'manage_kontrak': True, # Manajemen Kontrak devin
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