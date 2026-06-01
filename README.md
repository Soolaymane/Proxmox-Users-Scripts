# Proxmox-Users-Scripts

# pveum-pool-sync

Script Python de synchronisation automatique des pools Proxmox VE pour les utilisateurs LDAP.

## Description

Ce script interroge l'API Proxmox (`pveum`) pour récupérer la liste des utilisateurs LDAP et des pools existants, puis crée automatiquement un pool dédié pour chaque utilisateur LDAP qui n'en possède pas encore. Les droits `PVEAdmin` et `PVEPoolAdmin` lui sont alors attribués sur ce pool.

## Fonctionnement

1. Récupère la liste des utilisateurs Proxmox et filtre ceux authentifiés via `@ldap`
2. Récupère la liste des pools existants (format attendu : `pool-<username>`)
3. Pour chaque utilisateur LDAP sans pool associé :
   - Crée un nouveau pool nommé `pool-<username>`
   - Attribue le rôle `PVEAdmin` à l'utilisateur sur ce pool
   - Attribue le rôle `PVEPoolAdmin` à l'utilisateur sur ce pool

## Prérequis

- Python 3.x
- Module Python `pyyaml`
- Proxmox VE avec l'outil CLI `pveum` disponible dans le `PATH`
- Droits suffisants pour exécuter les commandes `pveum` (typiquement `root` ou un administrateur Proxmox)

## Installation

```bash
pip install pyyaml
```

## Utilisation

```bash
python pveum_pool_sync.py
```

> Le script doit être exécuté directement sur un nœud Proxmox VE (ou un environnement ayant accès à la CLI `pveum`).

## Permissions attribuées

| Rôle | Description |
|------|-------------|
| `PVEAdmin` | Administration complète des ressources du pool |
| `PVEPoolAdmin` | Gestion du pool (ajout/suppression de ressources) |

Les deux rôles sont appliqués avec l'option `--propagate`, ce qui propage les droits aux ressources enfants du pool.

## Conventions de nommage

- Les pools sont nommés selon le format : `pool-<username>`
- Seuls les utilisateurs avec le domaine d'authentification `@ldap` sont traités

## Exemple

Pour un utilisateur LDAP `jdupont@ldap`, le script crée :
- Le pool `/pool/pool-jdupont`
- Les ACL correspondantes sur `/pool/pool-jdupont`

## Avertissements

- Le script ne supprime pas les pools existants, même si l'utilisateur correspondant n'existe plus.
- Aucune gestion d'erreur n'est implémentée : une commande `pveum` en échec interrompra l'exécution.
- À utiliser avec précaution en production ; tester d'abord dans un environnement de développement.
