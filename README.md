Ansible Role: samba
=========

An Ansible Role that install and configures samba on RedHat/CentOS, Debian/Ubuntu and Fedora Linux systems.

Requirements
------------

This role requires pycryptodome python library.

Role Variables
--------------

**Available variables are listed below, along with default values (see defaults/main.yml):**

    #smb_file: server_smb.conf

Specify the file to be copied to the target device as samba configuration (smb.conf)

    #smb_users:
    #  - name: operator
    #    password: mypasswor12

Samba users to add (smbpasswd -a username)
**NOTE:** The users must exist on linux or it will fail

    #smb_users_remove:
    #  - operator

Samba users to remove (smbpasswd -x username)

    #smb_samba_export_all_ro: no

Set selinux to allow sharing of any standard directory read/only.

    #smb_samba_export_all_rw: no

Set selinux to allow sharing of any standard directory read/write.

    #smb_allow_smbd_anon_write: no

If you want to allow samba to modify public files used for public file transfer services. Files/Directories must be labeled public_content_rw_t, you must turn on the allow_smbd_anon_write boolean.

    #smb_enable_home_dirs: no

Allow samba to enable sharing home dirs

    #smb_create_home_dirs: no

Allow samba to create home dirs (e.g. via PAM)

    #smb_domain_controller: no

Allow samba to act as the domain controller, add users, groups and change passwords

    #smb_share_fusefs: no

Allow samba to export ntfs/fusefs volumes

    #smb_virt_use_samba: no

Allow virt to manage cifs files

    #smb_share_nfs: no

Allow samba to export NFS volumes

    #smb_run_unconfined: no

Allow samba to run unconfined scripts

    #smb_portmapper: no

Allow samba to act as a portmapper

    #smb_use_samba_home_dirs: no

If you want to support SAMBA home directories, you must turn on the use_samba_home_dirs boolean.

    #smb_sanlock_use_samba: no

Allow sanlock to manage cifs files

**The variables listed below do not need to be changed for targeted systems (see vars/main.yml):**

    smb_conf_dir: /etc/samba

Samba configuration directory.

    smb_conf_file: smb.conf

Samba configuration file.

    smb_owner: root
    smb_group: root
    smb_mode: '0640'

Owner, group and permissions to be set on configuration files.

    smb_service_names:

List of services names provided by samba.

    smb_packages:

List of packages to be installed to provide samba functionality.

Dependencies
------------

No dependencies.

Example Playbook
----------------

    - hosts: servers
      vars:
        smb_users:
          - name: nobody
            password: mypassword
        smb_samba_export_all_ro: no
        smb_samba_export_all_rw: no
        smb_allow_smbd_anon_write: no
        smb_enable_home_dirs: no
        smb_create_home_dirs: no
        smb_domain_controller: no
        smb_share_fusefs: no
        smb_virt_use_samba: no
        smb_share_nfs: no
        smb_run_unconfined: no
        smb_portmapper: no
        smb_use_samba_home_dirs: no
        smb_sanlock_use_samba: no
      roles:
         - { role: guidugli.samba }

License
-------

MIT / BSD

Author Information
------------------

This role was created in 2020 by Carlos Guidugli.
