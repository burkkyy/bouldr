import { ref, readonly } from "vue"
import usersApi, { type User } from "@/api/users-api"

const currentUser = ref<User | null>(null)

// Restore user from localStorage on module load
const savedUser = localStorage.getItem("currentUser")
if (savedUser) {
  try {
    currentUser.value = JSON.parse(savedUser)
  } catch {
    localStorage.removeItem("currentUser")
    localStorage.removeItem("currentUserId")
  }
}

function persistUser(user: User) {
  currentUser.value = user
  localStorage.setItem("currentUser", JSON.stringify(user))
  localStorage.setItem("currentUserId", String(user.id))
}

export function useCurrentUser() {
  async function login(username: string, password: string): Promise<User> {
    const user = await usersApi.login({ username, password })
    persistUser(user)
    return user
  }

  async function signup(username: string, password: string): Promise<User> {
    const user = await usersApi.create({ username, password })
    persistUser(user)
    return user
  }

  function logout() {
    currentUser.value = null
    localStorage.removeItem("currentUser")
    localStorage.removeItem("currentUserId")
  }

  return {
    currentUser: readonly(currentUser),
    login,
    signup,
    logout,
  }
}

export default useCurrentUser
