import http from "@/api/http-client"

export type Boulder = {
  id: number
  authorId: number
  regionId: number | null
  name: string
  description: string | null
  image: string | null // base64 data URL
  grade: number
  coordinates: string | null
  createdAt: string
  updatedAt: string
}

export type BoulderWhereOptions = {
  grade?: string
}

// eslint-disable-next-line @typescript-eslint/no-empty-object-type
export type BoulderFiltersOptions = {}

export type BoulderQueryOptions = {
  where?: BoulderWhereOptions
  filters?: BoulderFiltersOptions
  page?: number
  perPage?: number
}

export const bouldersApi = {
  async list(params: BoulderQueryOptions = {}): Promise<Boulder[]> {
    const { data } = await http.get("/api/boulders/", {
      params,
    })
    return data
  },
  async get(boulderId: number): Promise<Boulder> {
    const { data } = await http.get(`/api/boulders/${boulderId}`)
    return data
  },
  async create(attributes: Partial<Boulder>): Promise<Boulder> {
    const { data } = await http.post("/api/boulders/", {
      authorID: attributes.authorId,
      regionID: attributes.regionId,
      name: attributes.name,
      description: attributes.description,
      image: attributes.image,
      grade: attributes.grade,
      coordinates: attributes.coordinates,
    })
    return data
  },
  async update(boulderId: number, attributes: Partial<Boulder>): Promise<Boulder> {
    const body: Record<string, unknown> = {}
    if (attributes.name !== undefined) body.name = attributes.name
    if (attributes.description !== undefined) body.description = attributes.description
    if (attributes.image !== undefined) body.image = attributes.image
    if (attributes.grade !== undefined) body.grade = attributes.grade
    if (attributes.coordinates !== undefined) body.coordinates = attributes.coordinates
    if (attributes.regionId !== undefined) body.regionID = attributes.regionId
    const { data } = await http.patch(`/api/boulders/${boulderId}`, body)
    return data
  },
  async delete(boulderId: number): Promise<void> {
    await http.delete(`/api/boulders/${boulderId}`)
  },
}

export default bouldersApi
