import http from "@/api/http-client"

export type Send = {
  id: number
  boulderId: number
  userId: number
  rating: number | null
  sendType: number
  username?: string
  displayName?: string | null
  createdAt: string
  updatedAt: string
}

export type CreateSendAttributes = {
  boulderID: number
  userID: number
  sendType: number
  rating?: number | null
}

export const sendsApi = {
  async list(params: { boulderID?: number } = {}): Promise<Send[]> {
    const { data } = await http.get("/api/sends", { params })
    return data
  },
  async create(attributes: CreateSendAttributes): Promise<Send> {
    const { data } = await http.post("/api/sends/", attributes)
    return data
  },
}

export default sendsApi