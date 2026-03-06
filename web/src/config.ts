import { stripTrailingSlash } from "@/utils/strip-trailing-slash"

export const ENVIRONMENT = import.meta.env.MODE

const prodConfig = {
  domain: "https://dune-cx.us.auth0.com",
  clientId: "Bjuzy1WonTyMhuzVbC2BOwDFFg2D8091",
  audience: "thrive",
  apiBaseUrl: "",
  applicationName: "ARCHIEai",
}

const uatConfig = {
  domain: "https://dune-cx.us.auth0.com",
  clientId: "Bjuzy1WonTyMhuzVbC2BOwDFFg2D8091",
  audience: "thrive",
  apiBaseUrl: "",
  applicationName: "ARCHIEai - UAT",
}

const devConfig = {
  domain: "https://dune-cx.us.auth0.com",
  clientId: "Bjuzy1WonTyMhuzVbC2BOwDFFg2D8091",
  audience: "thrive",
  apiBaseUrl: "http://localhost:3000",
  applicationName: "ARCHIEai",
}

const localProductionConfig = {
  domain: "https://dune-cx.us.auth0.com",
  clientId: "Bjuzy1WonTyMhuzVbC2BOwDFFg2D8091",
  audience: "thrive",
  apiBaseUrl: "http://localhost:8080",
  applicationName: "ARCHIEai - DEV (production)",
}

let config = prodConfig

if (ENVIRONMENT === "production" && window.location.host === "localhost:8080") {
  config = localProductionConfig
} else if (window.location.host === "localhost:8080") {
  config = devConfig
} else if (window.location.host == "dune-thrive-uat.azurewebsites.net") {
  config = uatConfig
}

export const APPLICATION_NAME = config.applicationName
export const APPLICATION_ICON = "mdi-cable-data"

export const API_BASE_URL = config.apiBaseUrl

export const AUTH0_DOMAIN = stripTrailingSlash(config.domain)
export const AUTH0_AUDIENCE = config.audience
export const AUTH0_CLIENT_ID = config.clientId
