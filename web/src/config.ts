import { stripTrailingSlash } from "@/utils/strip-trailing-slash"

export const ENVIRONMENT = import.meta.env.MODE

const prodConfig = {
  domain: "",
  clientId: "",
  audience: "",
  apiBaseUrl: "",
  applicationName: "bouldr",
}

const devConfig = {
  domain: "",
  clientId: "",
  audience: "",
  apiBaseUrl: `http://localhost:${import.meta.env.VITE_API_PORT ?? 5001}`,
  applicationName: "bouldr",
}

const localProductionConfig = {
  domain: "",
  clientId: "",
  audience: "",
  apiBaseUrl: "http://localhost:8080",
  applicationName: "bouldr - DEV (production)",
}

let config = prodConfig

if (ENVIRONMENT === "production" && window.location.host === "localhost:8080") {
  config = localProductionConfig
} else if (window.location.host === "localhost:8080") {
  config = devConfig
}

export const APPLICATION_NAME = config.applicationName
export const APPLICATION_ICON = "mdi-cable-data"

export const API_BASE_URL = config.apiBaseUrl

export const AUTH0_DOMAIN = stripTrailingSlash(config.domain)
export const AUTH0_AUDIENCE = config.audience
export const AUTH0_CLIENT_ID = config.clientId
