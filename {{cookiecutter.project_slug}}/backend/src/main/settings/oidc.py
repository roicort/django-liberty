def userinfo(claims, user):
    claims["name"] = f"{user.first_name} {user.last_name}"
    claims["given_name"] = user.first_name
    claims["family_name"] = user.last_name
    claims["email"] = user.email

    return claims


"""
class CustomScopeClaims(ScopeClaims):
    info_foo = (
        _("Foo"),
        _("Some description for the scope."),
    )

    def scope_foo(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        # self.client - Client requesting this claims.
        dic = {
            "bar": "Something dynamic here",
        }

        return dic

    # If you want to change the description of the profile scope, you can redefine it.
    info_profile = (
        _("Profile"),
        _("Another description."),
    )
"""
