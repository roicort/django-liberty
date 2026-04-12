import NextAuth from "next-auth";
import type { OIDCConfig } from "@auth/core/providers";

export const { handlers, auth, signIn, signOut } = NextAuth({
  secret: process.env.AUTH_SECRET ?? process.env.NEXTAUTH_SECRET,
  providers: [
    {
      id: "django",
      name: "Django Liberty",
      type: "oidc",
      authorization: {
        params: {
          scope: "openid profile email",
        },
      },
      issuer: process.env.OIDC_ISSUER,
      clientId: process.env.OIDC_CLIENT_ID,
      clientSecret: process.env.OIDC_CLIENT_SECRET,
    } satisfies OIDCConfig,
  ],
  callbacks: {
    async jwt({ token, user, account, profile }) {
      if (user) {
        token.user = user;
      }
      if (profile) {
        token.profile = profile;
      }
      if (account) {
        token.account = account;
      }
      return token;
    },
    async session({ session, token }) {
      session.user = token.user;
      session.profile = token.profile;
      session.account = token.account;
      return session;
    },
  },
  debug: true,
});
