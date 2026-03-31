import http from "@/api/http-client"

export type User = {
  id: number
  username: string
  displayName: string | null
  createdAt: string
  updatedAt: string
}

export const usersApi = {
  async list(params: { username?: string } = {}): Promise<User[]> {
    const { data } = await http.get("/api/users", { params })
    return data
  },
  async create(attributes: { username: string }): Promise<User> {
    const { data } = await http.post("/api/users/", attributes)
    return data
  },
}

export default usersApi
