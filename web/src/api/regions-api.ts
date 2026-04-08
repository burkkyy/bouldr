import http from "@/api/http-client"

export type Region = {
  id: number
  type: string
  name: string
  parentId: number | null
  createdAt: string
  updatedAt: string
}

export const regionsApi = {
  async list(): Promise<Region[]> {
    const { data } = await http.get("/api/regions/")
    return data
  },
  async get(regionId: number): Promise<Region> {
    const { data } = await http.get(`/api/regions/${regionId}`)
    return data
  },
  async create(attributes: { type: string; name: string; parentId?: number | null }): Promise<Region> {
    const { data } = await http.post("/api/regions/", {
      type: attributes.type,
      name: attributes.name,
      parentID: attributes.parentId,
    })
    return data
  },
}

export default regionsApi