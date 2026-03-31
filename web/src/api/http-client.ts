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

httpClient.interceptors.response.use(null, async (error) => {
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
