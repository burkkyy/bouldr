import { ref, readonly } from "vue"
import usersApi, { type User } from "@/api/users-api"

const currentUser = ref<User | null>(null)

export function useCurrentUser() {
  async function login(username: string): Promise<User> {
    const users = await usersApi.list({ username })
    let user: User

    if (users.length > 0) {
      user = users[0]
    } else {
      user = await usersApi.create({ username })
    }

    currentUser.value = user
    return user
  }

  function logout() {
    currentUser.value = null
  }

  return {
    currentUser: readonly(currentUser),
    login,
    logout,
  }
}

export default useCurrentUser
