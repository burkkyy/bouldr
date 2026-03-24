import http from "@/api/http-client"

export type Boulder = {
  id: number
  authorId: number
  regionId: number | null
  name: string
  description: string | null
  image: string | null
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
    const { data } = await http.get("/api/boulders", {
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
  // async update(boulderId: number, attributes: Partial<Boulder>): Promise<{ boulder: Boulder }> {
  //   const { data } = await http.patch(`/api/boulders/${boulderId}`, attributes)
  //   return data
  // },
  // async delete(boulderId: number): Promise<void> {
  //   const { data } = await http.delete(`/api/boulders/${boulderId}`)
  //   return data
  // },
}

export default bouldersApi
