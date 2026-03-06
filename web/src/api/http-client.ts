import qs from "qs"
import axios from "axios"
import camelcaseKeys from "camelcase-keys"
import { API_BASE_URL } from "@/config"

export const httpClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  paramsSerializer: {
    serialize: (params) => {
      return qs.stringify(params, {
        arrayFormat: "indices",
        strictNullHandling: true,
      })
    },
  },
})

// Any status codes that falls outside the range of 2xx causes this function to trigger
httpClient.interceptors.response.use(null, async (error) => {
  // Auth0 error type is unknown but it sets the error.error property to "login_required"
  // Bounce the user if they hit a login required error when trying to access a protected route
  // It would probably be better to move this code to a route guard or something?
  if (error?.response?.data?.message) {
    throw new Error(error.response.data.message)
  } else if (error.message) {
    throw new Error(error.message)
  } else {
    throw new Error("An unknown error occurred")
  }
})
httpClient.interceptors.response.use((response) => {
  if (response?.data) {
    response.data = camelcaseKeys(response.data, { deep: true })
  }
  return response
})

export default httpClient
