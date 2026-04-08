const PASSWORD_RE = /^(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/

export function password(v: unknown): boolean | string {
  if (typeof v !== "string" || v.length < 8) {
    return "Password must be at least 8 characters"
  }
  if (!PASSWORD_RE.test(v)) {
    return "Password must contain at least one special character"
  }
  return true
}

export default password
