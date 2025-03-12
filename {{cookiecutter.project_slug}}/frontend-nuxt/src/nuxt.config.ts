// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  devtools: { enabled: true },
  modules: ["nuxt-oidc-auth"],
  oidc: {
    defaultProvider: "oidc",
    providers: {
      oidc: {
        // Configuración específica del proveedor OIDC
        clientId: process.env.OIDC_CLIENT_ID,
        clientSecret: process.env.OIDC_CLIENT_SECRET,
        authorizationUrl: "http://localhost:8000/oidc/authorize",
        tokenUrl: "http://localhost:8000/oidc/token",
        redirectUri: "http://localhost:3000/auth/oidc/callback",
        // Añade cualquier otra configuración necesaria para tu proveedor
      },
      // Puedes añadir más proveedores aquí si es necesario
    },
    middleware: {
      globalMiddlewareEnabled: false,
      customLoginPage: false,
    },
  },
});
