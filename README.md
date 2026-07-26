[![CI](https://github.com/guidugli/samba/actions/workflows/CI.yml/badgettps://github.com/guidugli/samba/actions/workflows/CI.yml)
[![Release](https://github.com/guidugli/sambakflows/release.yml/badge.svg](https://github.com/guidugli/samba/actions/workflows/release.yml)
[![Ansible .shields.io/badge/ansible--galaxy-guidugli.samba-blue.svg](https://galaxy.ansible.com/ui/standalone/roles/guidugli/samba/)
https://img.shields.io/badge/License-MIT-yellow.svg](LICENSE)

# Ansible Role: samba

Install and configure Samba on Linux systems.

This role:

- Installs Samba packages
- Deploys `smb.conf`
- Manages Samba users
- Configures Samba-related SELinux booleans
- Supports Ubuntu, Debian, and Fedora
- Includes Molecule test scenarios for both standard and systemd-based environments

---

## Requirements

### Control Node

- Ansible Core 2.17+
- `pycryptodome`
- Collections:
  - `ansible.posix >= 1.5.4`

### Managed Hosts

- Supported package manager
- Existing Linux accounts for users managed via `smb_users`

---

## Supported Platforms

The role is tested through Molecule against:

| Distribution | Versions |
|-------------|----------|
| Ubuntu | 24.04, 26.04 |
| Debian | 12, 13 |
| Fedora | 43, 44 |

---

## Variables

### smb_file

Name of the Samba configuration file located in the role `files/` directory.

Default:

```yaml
smb_file: ""
```

Example:

```yaml
smb_file: server_smb.conf
```

When specified, the file is deployed as:

```text
/etc/samba/smb.conf
```

The configuration is validated using:

```bash
testparm -s
```

before replacement.

---

### smb_users

List of Samba users to create or update.

Linux accounts must already exist.

Default:

```yaml
smb_users: []
```

Example:

```yaml
smb_users:
  - name: nobody
    password: "{{ vault_nobody_password }}"
```

> It is recommended to store passwords in Ansible Vault rather than in plaintext.

---

### smb_users_remove

List of Samba users to remove.

Default:

```yaml
smb_users_remove: []
```

Example:

```yaml
smb_users_remove:
  - olduser
```

---

### SELinux Booleans

All values default to:

```yaml
false
```

The role applies these settings only when SELinux is enabled.

| Variable | SELinux Boolean | Description |
|-----------|----------------|-------------|
| smb_samba_export_all_ro | samba_export_all_ro | Export directories read-only |
| smb_samba_export_all_rw | samba_export_all_rw | Export directories read/write |
| smb_allow_smbd_anon_write | allow_smbd_anon_write | Allow anonymous writes |
| smb_enable_home_dirs | samba_enable_home_dirs | Enable home directory shares |
| smb_create_home_dirs | samba_create_home_dirs | Allow automatic home directory creation |
| smb_domain_controller | samba_domain_controller | Domain controller functionality |
| smb_share_fusefs | samba_share_fusefs | Export FUSE filesystems |
| smb_virt_use_samba | virt_use_samba | Allow virtualization integration |
| smb_share_nfs | samba_share_nfs | Export NFS volumes |
| smb_run_unconfined | samba_run_unconfined | Run unconfined scripts |
| smb_portmapper | samba_portmapper | Enable portmapper support |
| smb_use_samba_home_dirs | use_samba_home_dirs | Samba home directories |
| smb_sanlock_use_samba | sanlock_use_samba | Sanlock CIFS support |

---

## Example Playbook

```yaml
---
- name: Configure Samba servers
  hosts: samba_servers
  become: true

  vars:
    smb_file: server_smb.conf

    smb_users:
      - name: nobody
        password: "{{ vault_nobody_password }}"

    smb_samba_export_all_ro: false
    smb_samba_export_all_rw: false

  roles:
    - role: guidugli.samba
```

---

## Molecule Testing

The role includes:

- Default container scenario
- Systemd-enabled scenario

Local validation:

```bash
ansible-galaxy collection install -r requirements.yml

yamllint .
ansible-lint .

molecule test -s default
molecule test -s systemd
```

---

## Execution Notes

### Privilege Model

The role intentionally does **not** define:

- `become`
- `become_user`
- `become_method`

Privilege escalation is controlled externally.

#### Molecule

Containers run as root:

```yaml
become: false
```

#### Real Hosts

Use:

```yaml
become: true
```

when required for:

- Package installation
- Service management
- SELinux modifications
- Samba account administration
- Configuration deployment under `/etc`

---

### Container and Systemd Behavior

The role can execute inside standard containers.

Service operations are executed only when systemd is detected:

```yaml
when: ansible_facts['service_mgr'] == 'systemd'
```

The dedicated Molecule systemd scenario validates service-related behavior.

---

## License

MIT

---

## Author

Carlos Guidugli
