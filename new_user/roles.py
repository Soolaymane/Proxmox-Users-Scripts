import yaml
import subprocess


users = yaml.safe_load(subprocess.check_output(
    ["pveum", "user", "list", "--output-format", "yaml"],
    text=True,
))

pools = yaml.safe_load(subprocess.check_output(
    ["pveum", "pool", "list", "--output-format", "yaml"],
    text=True,
))

users_l = [k['userid'].split('@')[0] for k in users if k['userid'].split('@')[1] == 'ldap']
pool_l = [
    k['poolid'].split('-', 1)[1]
    for k in pools
    if '-' in k['poolid']
]


for user in users_l:
    if user not in pool_l:
        new_pool = "pool-" + user
        subprocess.run(["pveum","pool","add",new_pool])
        subprocess.run(["pveum", "acl", "modify", "/pool/"+new_pool, "--users", user+"@ldap", "--roles", "PVEAdmin", "--propagate"])
        subprocess.run(["pveum", "acl", "modify", "/pool/"+new_pool, "--users", user+"@ldap", "--roles", "PVEPoolAdmin", "--propagate"])



