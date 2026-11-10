"""Deterministic separation-of-duty conflict check (stdlib only)."""


def effective_permissions(user, role_members, role_permissions):
    """Return the union of permissions granted by every role that contains user."""
    held = set()
    for role, members in role_members.items():
        if user in members:
            held.update(role_permissions.get(role, []))
    return held


def conflicts_for(user, role_members, role_permissions, constraints):
    """Return constraint pairs that both appear in the user's effective set."""
    held = effective_permissions(user, role_members, role_permissions)
    found = []
    for left, right in constraints:
        if left in held and right in held:
            found.append([left, right])
    return found


def audit(users, role_members, role_permissions, constraints):
    """Audit every user and count how many have at least one SoD conflict."""
    rows = []
    for user in users:
        found = conflicts_for(user, role_members, role_permissions, constraints)
        rows.append({
            "user": user,
            "permissions": sorted(effective_permissions(user, role_members, role_permissions)),
            "conflicts": found,
            "gapped": bool(found),
        })
    return rows
