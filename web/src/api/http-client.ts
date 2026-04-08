import qs from "qs"
import axios from "axios"
import camelcaseKeys from "camelcase-keys"
import { API_BASE_URL } from "@/config"
import { useSnack } from "@/use/use-snack"

const snack = useSnack()

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

httpClient.interceptors.request.use((config) => {
  const userId = localStorage.getItem("currentUserId")
  if (userId) {
    config.headers.Authorization = `Bearer ${userId}`
  }
  return config
})

httpClient.interceptors.response.use(null, async (error) => {
  const message = error?.response?.data?.error
    || error?.response?.data?.message
    || error.message
    || "An unknown error occurred"

  snack.error(message)
  throw new Error(message)
})
httpClient.interceptors.response.use((response) => {
  if (response?.data) {
    response.data = camelcaseKeys(response.data, { deep: true })
  }
  return response
})

export default httpClient
