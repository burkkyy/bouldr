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
  boulderId: number
  userId: number
  sendType: number
  rating?: number | null
}

export type UpdateSendAttributes = {
  sendType?: number
  rating?: number | null
}

export const sendsApi = {
  async list(params: { boulderId?: number } = {}): Promise<Send[]> {
    const { data } = await http.get("/api/sends/", {
      params: params.boulderId != null ? { boulderID: params.boulderId } : {},
    })
    return data
  },
  async create(attributes: CreateSendAttributes): Promise<Send> {
    const { data } = await http.post("/api/sends/", {
      boulderID: attributes.boulderId,
      userID: attributes.userId,
      sendType: attributes.sendType,
      rating: attributes.rating,
    })
    return data
  },
  async update(sendId: number, attributes: UpdateSendAttributes): Promise<Send> {
    const { data } = await http.patch(`/api/sends/${sendId}`, attributes)
    return data
  },
  async delete(sendId: number): Promise<void> {
    await http.delete(`/api/sends/${sendId}`)
  },
}

export default sendsApi
